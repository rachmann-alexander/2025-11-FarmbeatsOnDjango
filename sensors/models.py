from __future__ import annotations

from django.db import models
from django.utils import timezone


class SensorDevice(models.Model):
    class SensorType(models.TextChoices):
        AIR = "air", "Air Temperature & Humidity"

    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    sensor_type = models.CharField(max_length=32, choices=SensorType.choices)
    location = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class SensorReading(models.Model):
    device = models.ForeignKey(SensorDevice, related_name="readings", on_delete=models.CASCADE)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    recorded_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-recorded_at",)

    def __str__(self) -> str:
        return f"{self.device.name}: {self.humidity}% / {self.temperature}°C"
