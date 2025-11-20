from django.urls import path

from .views import LatestReadingsView

app_name = "sensors"

urlpatterns = [
    path("", LatestReadingsView.as_view(), name="latest_readings"),
]

