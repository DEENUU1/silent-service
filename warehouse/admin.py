from django.contrib import admin
from warehouse.models import Device, DeviceType


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_type')
    list_filter = ('device_type',)
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceType)
