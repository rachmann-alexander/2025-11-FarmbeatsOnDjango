from __future__ import annotations

import logging
from decimal import Decimal, ROUND_HALF_UP
from typing import List


class BaseSensor:
    """
    Shared utilities for physical or simulated sensors.
    Provides rolling average smoothing and Decimal coercion helpers.
    """

    null_value = Decimal("0")

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger("sensor_logger")
        self.init = False

    @staticmethod
    def _coerce_decimal(value: float | Decimal | int | None) -> Decimal:
        if value is None:
            return BaseSensor.null_value
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def rolling_average(
        self, new_value: float | Decimal | int | None, measurements: List[Decimal], window_size: int = 10
    ) -> Decimal:
        sanitized = self._coerce_decimal(new_value)
        measurements.append(sanitized)
        if len(measurements) > window_size:
            measurements.pop(0)
        average = sum(measurements) / len(measurements)
        return average.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


