from django.urls import path
from windows_monitor.views import (
    ComputerRawDataCreateView, computer_list, computer_detail,
)

app_name = "windows_monitor"

urlpatterns = [
    path("computer-data/", ComputerRawDataCreateView.as_view(), name="computer_raw_data_create"),
    path('computers/', computer_list, name='computer_list'),
    path('computers/<str:system_uuid>/', computer_detail, name='computer_detail'),
]
