#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-alerts/ampel/alert/AlertConsumer.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                10.10.2017
# Last Modified Date:  05.04.2023
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import sys
from collections.abc import Sequence
from contextlib import suppress
from signal import SIGINT, SIGTERM, default_int_handler, signal
from typing import TYPE_CHECKING, Any

from pymongo.errors import PyMongoError
from typing_extensions import Self

from ampel.abstract.AbsAlertSupplier import AbsAlertSupplier
from ampel.abstract.AbsEventUnit import AbsEventUnit
from ampel.abstract.AbsIngester import AbsIngester
from ampel.alert.AlertConsumerError import AlertConsumerError
from ampel.alert.AlertConsumerMetrics import AlertConsumerMetrics, stat_time
from ampel.alert.FilterBlocksHandler import FilterBlocksHandler
from ampel.base.AuxUnitRegister import AuxUnitRegister
from ampel.core.AmpelContext import AmpelContext
from ampel.core.EventHandler import EventHandler
from ampel.enum.EventCode import EventCode
from ampel.ingest.ChainedIngestionHandler import ChainedIngestionHandler
from ampel.log import VERBOSE, AmpelLogger, LogFlag
from ampel.log.AmpelLoggingError import AmpelLoggingError
from ampel.log.LightLogRecord import LightLogRecord
from ampel.log.utils import report_exception
from ampel.model.AlertConsumerModel import AlertConsumerModel
from ampel.model.ingest.CompilerOptions import CompilerOptions
from ampel.model.UnitModel import UnitModel
from ampel.util.freeze import recursive_unfreeze
from ampel.util.mappings import get_by_path, merge_dict

if TYPE_CHECKING:
	from ampel.alert.FilterBlock import FilterBlock
	from ampel.protocol.AmpelAlertProtocol import AmpelAlertProtocol

class AlertConsumer(AbsEventUnit, AlertConsumerModel):
	"""
	Class handling the processing of alerts (T0 level).
	For each alert, following tasks are performed:

	* Load the alert
	* Filter alert based on the configured T0 filter
	* Ingest alert based on the configured ingester
	"""

	#: Flag to use for log records with a level between INFO and WARN
	shout: int = LogFlag.SHOUT


	@classmethod
	def from_process(cls, context: AmpelContext, process_name: str, override: None | dict = None):
		"""
		Convenience method instantiating an AlertConsumer using the config entry from a given T0 process.
		
		Example::
		    
		  AlertConsumer.from_process(
		      context, process_name="VAL_TEST2/T0/ztf_uw_public", override={'iter_max': 100}
		  )
		"""
		args = context.get_config().get(f"process.{process_name}.processor.config", dict)
		if args is None:
			raise ValueError(f"process.{process_name}.processor.config is None")

		if override:
			args = merge_dict(recursive_unfreeze(args), override) # type: ignore

		return cls(context=context, **args)


	@classmethod # override (just set defaults for templates)
	def new(cls,
		templates: str | Sequence[str] = ('resolve_run_time_aliases', 'hash_t2_config'),
		**kwargs
	) -> Self:
		""" Hashes t2 unit configs on the fly (to use with jupyter for ex.) """
		return super().new(templates=templates, **kwargs)


	def __init__(self, **kwargs) -> None:
		"""
		:raises:
			:class:`ValueError` if no process can be loaded or if a process is
			associated with an unknown channel
		"""

		if kwargs.get("context") is None:
			raise ValueError("An ampel context is required")

		if isinstance(kwargs['directives'], dict):
			kwargs['directives'] = [kwargs['directives']]

		#: Allow str (shortcut for a configless UnitModel(unit=str)) for convenience
		for el in ('shaper', 'supplier'):
			if el in kwargs and isinstance(kwargs[el], str):
				kwargs[el] = {"unit": kwargs[el]}

		# Allow loading compiler opts via aux unit for convenience
		if isinstance(copts := kwargs.get('compiler_opts'), str):
			kwargs['compiler_opts'] = AuxUnitRegister.new_unit(
				model=UnitModel(unit=copts)
			)

		logger = AmpelLogger.get_logger(
			console=kwargs['context'].config.get(
				f"logging.{self.log_profile}.console", dict
			)
		)

		super().__init__(**kwargs)

		self._alert_supplier = AuxUnitRegister.new_unit(
			model = self.supplier,
			sub_type = AbsAlertSupplier
		)

		if AmpelLogger.has_verbose_console(self.context, self.log_profile):
			logger.log(VERBOSE, "AlertConsumer setup")

		# Load filter blocks
		self._fbh = FilterBlocksHandler(
			self.context, logger, self.directives, self.process_name, self.db_log_format
		)

		#signal(SIGTERM, self.register_sigterm)
		signal(SIGTERM, default_int_handler) # type: ignore[arg-type]
		logger.info("AlertConsumer setup completed")


	@property
	def alert_supplier(self) -> AbsAlertSupplier:
		return self._alert_supplier


	def register_signal(self, signum: int, frame) -> None:
		""" Executed when SIGINT/SIGTERM is emitted during alert processing """
		if self._cancel_run == 0:
			self.print_feedback(signum, "(after processing of current alert)")
			self._cancel_run: int = signum


	def chatty_interrupt(self, signum: int, frame) -> None:
		""" Executed when SIGINT/SIGTERM is emitted during alert supplier execution """
		self.print_feedback(signum, "(outside of alert processing)")
		self._cancel_run = signum
		default_int_handler(signum, frame)


	def set_cancel_run(self, reason: AlertConsumerError = AlertConsumerError.CONNECTIVITY) -> None:
		"""
		Cancels current processing of alerts (when DB becomes unresponsive for example).
		Called in main loop or by DBUpdatesBuffer in case of un-recoverable errors.
		"""
		if self._cancel_run == 0:
			self.print_feedback(reason, "after processing of current alert")
			self._cancel_run = reason


	def get_ingestion_handler(self,
		event_hdlr: EventHandler,
		ingester: AbsIngester,
		logger: AmpelLogger
	) -> ChainedIngestionHandler:

		return ChainedIngestionHandler(
			self.context, self.shaper, self.directives, ingester,
			event_hdlr.get_run_id(), tier = 0, logger = logger,
			trace_id = {'alertconsumer': self._trace_id},
			compiler_opts = self.compiler_opts or CompilerOptions()
		)


	def process_alerts(self) -> None:
		"""
		Convenience method to process all alerts from a given loader until it dries out
		"""
		processed_alerts = self.iter_max
		while processed_alerts == self.iter_max:
			processed_alerts = self.run()


	def proceed(self, event_hdlr: EventHandler) -> int:
		"""
		Process alerts using internal alert_loader/alert_supplier

		:returns: Number of alerts processed
		:raises: LogFlushingError, PyMongoError
		"""

		# Setup stats
		#############

		stats = AlertConsumerMetrics(self._fbh.chan_names)

		event_hdlr.set_tier(0)
		run_id = event_hdlr.get_run_id()

		# Setup logging
		###############

		logger = AmpelLogger.from_profile(
			self.context, self.log_profile, run_id,
			base_flag = LogFlag.T0 | LogFlag.CORE | self.base_log_flag
		)

		self._alert_supplier.set_logger(logger)

		if event_hdlr.resources:
			for k, v in event_hdlr.resources.items():
				self._alert_supplier.add_resource(k, v)

		if logger.verbose:
			logger.log(VERBOSE, "Pre-run setup")

		# DBLoggingHandler formats, saves and pushes log records into the DB
		if db_logging_handler := logger.get_db_logging_handler():
			db_logging_handler.auto_flush = False

		any_filter = any([fb.filter_model for fb in self._fbh.filter_blocks])

		# Loop variables
		iter_max = self.iter_max
		if self.iter_max != self._defaults['iter_max']:
			logger.info(f"Using custom iter_max: {self.iter_max}")

		self._cancel_run = 0
		iter_count = 0
		err = 0

		assert self._fbh.chan_names is not None
		reduced_chan_names: str | list[str] = self._fbh.chan_names[0] \
			if len(self._fbh.chan_names) == 1 else self._fbh.chan_names
		fblocks = self._fbh.filter_blocks

		if any_filter:
			filter_results: list[tuple[int, bool | int]] = []
		else:
			filter_results = [(i, True) for i, fb in enumerate(fblocks)]

		# Shortcuts
		def report_filter_error(e: Exception, alert: "AmpelAlertProtocol", fblock: "FilterBlock"):
			self._report_ap_error(
				e, event_hdlr, logger,
				extra = {'a': alert.id, 'section': 'filter', 'c': fblock.channel}
			)

		def report_ingest_error(e: Exception, alert: "AmpelAlertProtocol", filter_results: Sequence[tuple[int, bool|int]]):
			self._report_ap_error(
				e, event_hdlr, logger, extra={
					'a': alert.id, 'section': 'ingest',
					'c': [self.directives[el[0]].channel for el in filter_results]
				}
			)

		# Process alerts
		################

		# The extra is just a feedback for the console stream handler
		logger.log(self.shout, "Processing alerts", extra={'r': run_id})

		with (
			# Build set of stock ids for autocomplete, if needed, and flushes
			# rejected alert registers at the end of the context
			self._fbh.ready(logger, run_id),
			# Flush at end of context
			logger,
			# Set up alert supplier, and tear down at end of context
			self._alert_supplier,
			# Set up ingester, and tear down at end of context
			self.context.loader.new_context_unit(
				self.ingester,
				context = self.context,
				run_id = run_id,
				tier = 0,
				process_name = self.process_name,
				error_callback = self.set_cancel_run,
				acknowledge_callback = self._alert_supplier.acknowledge,
				logger = logger,
				sub_type = AbsIngester,
			) as ingester
		):
			try:

				# Set ingesters up
				ing_hdlr = self.get_ingestion_handler(event_hdlr, ingester, logger)

				chatty_interrupt = self.chatty_interrupt
				register_signal = self.register_signal

				# Iterate over alerts
				for alert in self._alert_supplier:

					# Allow execution to complete for this alert (loop exited after ingestion of current alert)
					signal(SIGINT, register_signal)
					signal(SIGTERM, register_signal)

					# Associate upcoming log entries with the current transient id
					stock_id = alert.stock

					if any_filter:

						filter_results = []

						# Loop through filter blocks
						for fblock in fblocks:

							try:
								# Apply filter (returns None/False in case of rejection or True/int in case of match)
								res = fblock.filter(alert)
								if res[1]:
									filter_results.append(res) # type: ignore[arg-type]

							# Unrecoverable (logging related) errors
							except (PyMongoError, AmpelLoggingError) as e:  # noqa: PERF203
								print(f"{e.__class__.__name__}: abording run() procedure")
								report_filter_error(e, alert, fblock)
								raise e

							# Possibly tolerable errors (could be an error from a contributed filter)
							except Exception as e:

								if db_logging_handler:
									fblock.forward(db_logging_handler, stock=stock_id, extra={'a': alert.id})

								report_filter_error(e, alert, fblock)

								if self.raise_exc:
									raise e
								if self.error_max:
									err += 1
								if err == self.error_max:
									logger.error("Max number of error reached, breaking alert processing")
									self.set_cancel_run(AlertConsumerError.TOO_MANY_ERRORS)
					else:
						# if bypassing filters, track passing rates at top level
						for counter in stats.filter_accepted:
							counter.inc()

					with ingester.group([alert]):

						if filter_results:

							stats.accepted.inc()

							try:
								alert_extra: dict[str, Any] = {'alert': alert.id}
								if self.include_alert_extra_with_keys and alert.extra:
									for key, path in self.include_alert_extra_with_keys.items():
										alert_extra[key] = get_by_path(alert.extra, path)
								with stat_time.labels("ingest").time():
									ing_hdlr.ingest(
										alert.datapoints, filter_results, stock_id, alert.tag,
										alert_extra, alert.extra.get('stock') if alert.extra else None
									)
							except Exception as e:
								print(f"{e.__class__.__name__}: abording run() procedure")
								report_ingest_error(e, alert, filter_results)
								raise e

						else:

							# All channels reject this alert
							# no log entries goes into the main logs collection sinces those are redirected to Ampel_rej.

							# So we add a notification manually. For that, we don't use logger
							# cause rejection messages were alreary logged into the console
							# by the StreamHandler in channel specific RecordBufferingHandler instances.
							# So we address directly db_logging_handler, and for that, we create
							# a LogDocument manually.
							lr = LightLogRecord(logger.name, LogFlag.INFO | logger.base_flag)
							lr.stock = stock_id
							lr.channel = reduced_chan_names # type: ignore[assignment]
							lr.extra = {'a': alert.id, 'allout': True}
							if db_logging_handler:
								db_logging_handler.handle(lr)

					iter_count += 1
					stats.alerts.inc()

					if db_logging_handler:
						db_logging_handler.check_flush()

					if iter_count == iter_max:
						logger.info("Reached max number of iterations")
						break

					# Exit if so requested (SIGINT, error registered by DBUpdatesBuffer, ...)
					if self._cancel_run > 0:
						break

					# Restore system default sig handling so that KeyBoardInterrupt
					# can be raised during supplier execution
					signal(SIGINT, chatty_interrupt)
					signal(SIGTERM, chatty_interrupt)

			# Executed if SIGINT was sent during supplier execution
			except KeyboardInterrupt:
				pass

			except Exception as e:
				event_hdlr.handle_error(e, logger)

				if self.raise_exc:
					raise e

			# Also executed after SIGINT and SIGTERM
			finally:

				if self._cancel_run > 0:
					print("")
					logger.info("Processing interrupted")
				else:
					logger.log(self.shout, "Processing completed")

		if self.exit_if_no_alert and iter_count == 0:
			sys.exit(self.exit_if_no_alert)

		# Return number of processed alerts
		return iter_count


	@staticmethod
	def _report_ap_error(
		arg_e: Exception,
		event_hdlr: EventHandler,
		logger: AmpelLogger,
		extra: None | dict[str, Any] = None
	) -> None:
		"""
		:param extra: optional extra key/value fields to add to 'trouble' doc
		"""

		event_hdlr.set_code(EventCode.EXCEPTION)
		info: Any = {
			'process': event_hdlr.process_name,
			'run': event_hdlr.get_run_id()
		}

		if extra:
			for k, v in extra.items():
				info[k] = v

		# Try to insert doc into trouble collection (raises no exception)
		# Possible exception will be logged out to console in any case
		report_exception(event_hdlr.db, logger, exc=arg_e, info=info)


	@staticmethod
	def print_feedback(arg: Any, suffix: str = "") -> None:
		print("") # ^C in console
		with suppress(Exception):
			arg = AlertConsumerError(arg)
		s = f"[{arg.name if isinstance(arg, AlertConsumerError) else arg}] Interrupting run {suffix}"
		print("+" * len(s))
		print(s)
		print("+" * len(s))
