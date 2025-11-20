from __future__ import annotations

import logging
import time
from typing import List

from django.db import transaction
from django.utils import timezone

from ..hardware.air_temperature_humidity import AirTemperatureHumiditySensor
from ..models import SensorDevice, SensorReading


class SensorCollector:
    """
    High-level service that interacts with physical/simulated sensors
    and persists structured readings into the database.
    """

    def __init__(self):
        self.logger = logging.getLogger("sensor_logger")
        self.air_sensor = AirTemperatureHumiditySensor()

    def collect_air_sample(self) -> SensorReading:
        device = self._get_or_create_air_device()
        humidity, temperature = self.air_sensor.read()

        with transaction.atomic():
            reading = SensorReading.objects.create(
                device=device,
                humidity=humidity,
                temperature=temperature,
                recorded_at=timezone.now(),
            )

        self.logger.info(
            "Stored air reading from %s: humidity=%s%% temperature=%s°C",
            device.name,
            humidity,
            temperature,
        )
        return reading

    def collect_air_samples(self, samples: int = 1, interval_seconds: float = 2.0) -> List[SensorReading]:
        samples = max(1, int(samples))
        interval_seconds = max(0.0, float(interval_seconds))

        readings: List[SensorReading] = []
        for index in range(samples):
            readings.append(self.collect_air_sample())
            if index < samples - 1 and interval_seconds:
                time.sleep(interval_seconds)
        return readings

    def _get_or_create_air_device(self) -> SensorDevice:
        device, created = SensorDevice.objects.get_or_create(
            slug="air-temperature-humidity",
            defaults={
                "name": "Air Temperature & Humidity",
                "sensor_type": SensorDevice.SensorType.AIR,
                "location": "Field Station",
            },
        )
        if created:
            self.logger.info("Registered new sensor device: %s", device.name)
        return device

