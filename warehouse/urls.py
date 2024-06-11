from django.urls import path
from warehouse.views import (
    DeviceListView,
    CreateDeviceView,
    DeviceDetailView,
)

app_name = "warehouse"

urlpatterns = [
    path('', DeviceListView.as_view(), name='device-list'),
    path('create/', CreateDeviceView.as_view(), name='device-create'),
    path('<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
]
