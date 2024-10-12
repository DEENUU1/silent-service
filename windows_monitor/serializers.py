from rest_framework.serializers import ModelSerializer
from windows_monitor.models import ComputerRawData


class ComputerRawDataInputSerializer(ModelSerializer):
    class Meta:
        model = ComputerRawData
        fields = (
            "system_uuid",
            "data_system",
            "data_disk",
            "data_disk_2",
            "data_system_2",
            "data_bios",
            "sensor_data"
        )
