from django.contrib import admin
from django.urls import path

from .views import SensorView, SensorRetrieveUpdate, MeasurementAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sensors/', SensorView.as_view()),
    path('sensors/<pk>/', SensorRetrieveUpdate.as_view()),
    path('measurements/', MeasurementAPIView.as_view()),
]
