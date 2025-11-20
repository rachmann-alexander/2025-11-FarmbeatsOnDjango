from django.contrib import admin

from .models import SensorDevice, SensorReading


@admin.register(SensorDevice)
class SensorDeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "sensor_type", "location", "is_active", "created_at")
    list_filter = ("sensor_type", "is_active")
    search_fields = ("name", "location", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ("device", "humidity", "temperature", "recorded_at")
    list_filter = ("device__name",)
    search_fields = ("device__name",)
    date_hierarchy = "recorded_at"
