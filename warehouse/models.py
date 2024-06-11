from django.db import models
from utils.base_model import BaseModel


class DeviceType(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Device Type"
        verbose_name_plural = "Device Types"


class Device(BaseModel):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Device"
        verbose_name_plural = "Devices"
