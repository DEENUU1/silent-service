from typing import Any

from windows_monitor.models import ComputerRawData


class ComputerDataService:
    def __init__(self):
        self.model = ComputerRawData

    def create_computer_data(self, data: dict[str, Any]) -> ComputerRawData:
        return self.model.objects.create(**data)
