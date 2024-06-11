from django.urls import path
from warehouse.views import (
    DeviceListView,
    CreateDeviceView,
    DeviceDetailView,
    DeviceUpdateView,
    DeleteDeviceView,

)

app_name = "warehouse"

urlpatterns = [
    path('', DeviceListView.as_view(), name='device-list'),
    path('create/', CreateDeviceView.as_view(), name='device-create'),
    path('<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('<int:pk>/update/', DeviceUpdateView.as_view(), name='device-update'),
    path('<int:pk>/delete/', DeleteDeviceView.as_view(), name='device-delete'),
]
