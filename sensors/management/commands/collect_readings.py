from __future__ import annotations

import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from sensors.services.collector import SensorCollector


class Command(BaseCommand):
    help = "Collect sensor readings from the hardware layer and persist them in the database."

    def add_arguments(self, parser):
        parser.add_argument("--samples", type=int, default=1, help="Number of readings to capture.")
        parser.add_argument(
            "--interval",
            type=float,
            default=2.0,
            help="Seconds to wait between samples (ignored when only one sample is captured).",
        )

    def handle(self, *args, **options):
        self._reset_runtime_log()
        logger = logging.getLogger("sensor_logger")
        collector = SensorCollector()

        samples = max(1, options["samples"])
        interval = max(0.0, options["interval"])
        logger.info("Starting collection run: samples=%s interval=%ss", samples, interval)

        readings = collector.collect_air_samples(samples, interval)
        for index, reading in enumerate(readings, start=1):
            self.stdout.write(
                self.style.SUCCESS(
                    f"[{index}/{samples}] {reading.device.name}: "
                    f"humidity={reading.humidity}% temperature={reading.temperature}°C"
                )
            )

        logger.info("Completed collection run, stored %s readings", len(readings))

    def _reset_runtime_log(self) -> None:
        runtime_path = Path(settings.RUNTIME_LOG_PATH)
        runtime_path.write_text("")
        logging.getLogger("sensor_logger").info("runtime_log.log truncated for new run")

