from django.views.generic import ListView

from .models import SensorReading


class LatestReadingsView(ListView):
    """
    Simple dashboard that renders the most recent sensor readings.
    """

    template_name = "sensors/latest_readings.html"
    context_object_name = "readings"
    paginate_by = 25

    def get_queryset(self):
        return (
            SensorReading.objects.select_related("device")
            .order_by("-recorded_at")
        )
