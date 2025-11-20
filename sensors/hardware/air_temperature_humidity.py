from __future__ import annotations

import random
import time
from decimal import Decimal
from typing import Tuple

from .base import BaseSensor

try:
    from seeed_dht import DHT
except ImportError:  # pragma: no cover - optional hardware dependency
    DHT = None


class AirTemperatureHumiditySensor(BaseSensor):
    """
    Reads humidity and temperature from a DHT sensor (or a simulated source).
    Makes two attempts to mitigate transient zero readings, then smooths values
    using a rolling average window.
    """

    def __init__(self, dht_pin: int = 16, dht_type: str = "11", retry_delay: float = 0.1):
        super().__init__("air_temperature_humidity")
        self.dht_pin = dht_pin
        self.dht_type = dht_type
        self.retry_delay = retry_delay
        self.humidity_measurements: list[Decimal] = []
        self.temperature_measurements: list[Decimal] = []
        self.sensor = None
        self.setup()

    def setup(self) -> None:
        if DHT is None:
            self.logger.warning(
                "AirTemperatureHumiditySensor.setup: seeed_dht not available, falling back to simulated readings"
            )
            self.sensor = None
            self.init = True
            return

        try:
            self.sensor = DHT(self.dht_type, self.dht_pin)
            self.init = True
            self.logger.info("AirTemperatureHumiditySensor.setup: hardware sensor initialised on pin %s", self.dht_pin)
        except Exception as exc:  # pragma: no cover - hardware failure path
            self.logger.error("AirTemperatureHumiditySensor.setup failed: %s", exc)
            self.sensor = None
            self.init = True  # allow simulated fallback

    def read(self) -> Tuple[Decimal, Decimal]:
        air_humidity, air_temperature = self._take_readings()

        if air_humidity == self.null_value or air_temperature == self.null_value:
            time.sleep(self.retry_delay)
            re_h, re_t = self._take_readings()
            if air_humidity == self.null_value:
                air_humidity = re_h
            if air_temperature == self.null_value:
                air_temperature = re_t

        air_humidity = self.rolling_average(air_humidity, self.humidity_measurements, 10)
        air_temperature = self.rolling_average(air_temperature, self.temperature_measurements, 10)

        return air_humidity, air_temperature

    def _take_readings(self) -> Tuple[Decimal, Decimal]:
        if not self.init:
            self.setup()

        if self.sensor is None:
            return self._simulate_reading()

        try:
            air_humidity, air_temperature = self.sensor.read()
            return self._coerce_decimal(air_humidity), self._coerce_decimal(air_temperature)
        except Exception as exc:  # pragma: no cover - hardware failure path
            self.logger.error("AirTemperatureHumiditySensor.read failed: %s", exc)
            self.sensor = None
            return self._simulate_reading()

    def _simulate_reading(self) -> Tuple[Decimal, Decimal]:
        humidity = Decimal(str(random.uniform(40, 70))).quantize(Decimal("0.01"))
        temperature = Decimal(str(random.uniform(18, 28))).quantize(Decimal("0.01"))
        self.logger.debug("Simulated reading humidity=%s temperature=%s", humidity, temperature)
        return humidity, temperature
