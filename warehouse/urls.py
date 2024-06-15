from django.urls import path
from warehouse.views import (
    DeviceListView,
    DeviceCreateView,
    DeviceDetailView,
    DeviceUpdateView,
    DeviceDeleteView,
    some_view,
    DeviceTypeUpdateView,
    DeviceTypeDeleteView,
    DeviceTypeDetailView,
    DeviceTypeListView,
    DeviceTypeCreateView,
)

app_name = "warehouse"

urlpatterns = [
    path('', DeviceListView.as_view(), name='device-list'),
    path('create/', DeviceCreateView.as_view(), name='device-create'),
    # path('<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('<int:pk>/update/', DeviceUpdateView.as_view(), name='device-update'),
    path('<int:pk>/delete/', DeviceDeleteView.as_view(), name='device-delete'),
    path('some_view/', some_view, name='some_view'),

    path('device_type/<int:pk>/', DeviceTypeDetailView.as_view(), name='device-type-detail'),
    path('device_type/<int:pk>/update/', DeviceTypeUpdateView.as_view(), name='device-type-update'),
    path('device_type/<int:pk>/delete/', DeviceTypeDeleteView.as_view(), name='device-type-delete'),
    path('device_type/', DeviceTypeListView.as_view(), name='device-type-list'),
    path('device_type/create/', DeviceTypeCreateView.as_view(), name='device-type-create'),
]
