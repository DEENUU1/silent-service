from django.contrib import admin
from windows_monitor.models import (
    ComputerRawData, Computer, Bios, Monitor, MotherBoard, Mouse, Printer,
    SoundDevice, VideoController, NetworkAdapter, Memory, CPU, Core,
    Keyboard, Disk, Partition, Volume, System, GPUSensor, CPUSensor, MemorySensor, StorageSensor
)


@admin.register(ComputerRawData)
class ComputerRawDataAdmin(admin.ModelAdmin):
    list_display = ('system_uuid', 'created_at', 'updated_at')
    search_fields = ('system_uuid',)
    list_filter = ('created_at', 'updated_at')


@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('system_uuid', 'created_at', 'updated_at')
    search_fields = ('system_uuid',)
    list_filter = ('created_at', 'updated_at')


@admin.register(Bios)
class BiosAdmin(admin.ModelAdmin):
    list_display = ('computer', 'name', 'version', 'manufacturer')
    search_fields = ('name', 'version', 'manufacturer')
    list_filter = ('status', 'created_at', 'updated_at')


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('computer', 'caption', 'manufacturer', 'serial_number', 'active')
    search_fields = ('caption', 'manufacturer', 'serial_number')
    list_filter = ('active', 'year_of_manufacture', 'created_at', 'updated_at')


@admin.register(MotherBoard)
class MotherBoardAdmin(admin.ModelAdmin):
    list_display = ('computer', 'manufacturer', 'product', 'serial_number')
    search_fields = ('manufacturer', 'product', 'serial_number')
    list_filter = ('created_at', 'updated_at')


@admin.register(Mouse)
class MouseAdmin(admin.ModelAdmin):
    list_display = ('computer', 'caption', 'manufacturer', 'number_of_buttons')
    search_fields = ('caption', 'manufacturer')
    list_filter = ('number_of_buttons', 'created_at', 'updated_at')


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('computer', 'caption', 'name', 'default', 'local', 'network', 'shared')
    search_fields = ('caption', 'name')
    list_filter = ('default', 'local', 'network', 'shared', 'created_at', 'updated_at')


@admin.register(SoundDevice)
class SoundDeviceAdmin(admin.ModelAdmin):
    list_display = ('computer', 'caption', 'manufacturer', 'product_name')
    search_fields = ('caption', 'manufacturer', 'product_name')
    list_filter = ('created_at', 'updated_at')


@admin.register(VideoController)
class VideoControllerAdmin(admin.ModelAdmin):
    list_display = ('computer', 'caption', 'manufacturer', 'video_processor')
    search_fields = ('caption', 'manufacturer', 'video_processor')
    list_filter = ('created_at', 'updated_at')


@admin.register(NetworkAdapter)
class NetworkAdapterAdmin(admin.ModelAdmin):
    list_display = ('computer', 'caption', 'manufacturer', 'product_name', 'mac_address')
    search_fields = ('caption', 'manufacturer', 'product_name', 'mac_address')
    list_filter = ('adapter_type', 'created_at', 'updated_at')


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ('computer', 'bank_label', 'capacity', 'speed', 'serial_number')
    search_fields = ('bank_label', 'serial_number')
    list_filter = ('speed', 'created_at', 'updated_at')


@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = ('computer', 'caption', 'name', 'number_of_cores', 'number_of_logical_processors')
    search_fields = ('caption', 'name', 'processor_id')
    list_filter = ('number_of_cores', 'number_of_logical_processors', 'created_at', 'updated_at')


@admin.register(Core)
class CoreAdmin(admin.ModelAdmin):
    list_display = ('computer', 'cpu', 'name', 'percent_processor_time')
    search_fields = ('name',)
    list_filter = ('percent_processor_time', 'created_at', 'updated_at')


@admin.register(Keyboard)
class KeyboardAdmin(admin.ModelAdmin):
    list_display = ('computer', 'caption', 'name', 'number_of_function_keys')
    search_fields = ('caption', 'name')
    list_filter = ('number_of_function_keys', 'created_at', 'updated_at')


@admin.register(Disk)
class DiskAdmin(admin.ModelAdmin):
    list_display = ('computer', 'caption', 'model', 'size', 'partitions', 'serial_number')
    search_fields = ('caption', 'model', 'serial_number')
    list_filter = ('partitions', 'created_at', 'updated_at')


@admin.register(Partition)
class PartitionAdmin(admin.ModelAdmin):
    list_display = ('computer', 'disk', 'name', 'bootable', 'size', 'index')
    search_fields = ('name',)
    list_filter = ('bootable', 'created_at', 'updated_at')


@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_display = ('computer', 'partition', 'caption', 'name', 'file_system', 'size', 'free_space')
    search_fields = ('caption', 'name', 'volume_serial_number')
    list_filter = ('file_system', 'created_at', 'updated_at')


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('computer', 'caption', 'cs_name', 'os_architecture', 'version', 'status')
    search_fields = ('caption', 'cs_name', 'registered_user', 'serial_number')
    list_filter = ('os_architecture', 'status', 'created_at', 'updated_at')


@admin.register(CPUSensor)
class CPUSensorAdmin(admin.ModelAdmin):
    list_display = ('computer', 'name', 'value', 'sensor_type')
    search_fields = ('name', 'sensor_type')
    list_filter = ('created_at', 'updated_at')


@admin.register(MemorySensor)
class MemorySensorAdmin(admin.ModelAdmin):
    list_display = ('computer', 'name', 'value', 'sensor_type')
    search_fields = ('name', 'sensor_type')
    list_filter = ('created_at', 'updated_at')


@admin.register(GPUSensor)
class GPUSensorAdmin(admin.ModelAdmin):
    list_display = ('computer', 'name', 'value', 'sensor_type')
    search_fields = ('name', 'sensor_type')
    list_filter = ('created_at', 'updated_at')


@admin.register(StorageSensor)
class StorageSensorAdmin(admin.ModelAdmin):
    list_display = ('computer', 'name', 'value', 'sensor_type')
    search_fields = ('name', 'sensor_type')
    list_filter = ('created_at', 'updated_at')
