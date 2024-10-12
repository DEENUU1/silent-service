from django.db import models


class ComputerRawData(models.Model):
    system_uuid = models.CharField(max_length=250, null=False, blank=False)
    data_system = models.JSONField(null=True, blank=True)
    data_disk = models.JSONField(null=True, blank=True)
    data_disk_2 = models.JSONField(null=True, blank=True)
    data_system_2 = models.JSONField(null=True, blank=True)
    data_bios = models.JSONField(null=True, blank=True)
    sensor_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.system_uuid

    class Meta:
        verbose_name = "Computer Raw Data"
        verbose_name_plural = "Computer Raw Data"
        ordering = ["-created_at"]


class Computer(models.Model):
    system_uuid = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.system_uuid

    class Meta:
        verbose_name = "Computer"
        verbose_name_plural = "Computer"
        ordering = ["-created_at"]


class Bios(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    version = models.CharField(max_length=250, null=False, blank=False)
    target_os = models.IntegerField()
    minor_version = models.IntegerField()
    major_version = models.IntegerField()
    status = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    manufacturer = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bios"
        verbose_name_plural = "Bios"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Monitor(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    monitor_type = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    pixel_x_inch = models.IntegerField()
    pixel_y_inch = models.IntegerField()
    active = models.BooleanField(default=True)
    manufacturer = models.CharField(max_length=250, null=False, blank=False)
    product_code = models.CharField(max_length=250, null=False, blank=False)
    serial_number = models.CharField(max_length=250, null=False, blank=False)
    user_friendly_name = models.CharField(max_length=250, null=False, blank=False)
    week_of_manufacture = models.IntegerField()
    year_of_manufacture = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Monitor"
        verbose_name_plural = "Monitor"
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption


class MotherBoard(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=250, null=False, blank=False)
    product = models.CharField(max_length=250, null=False, blank=False)
    serial_number = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "MotherBoard"
        verbose_name_plural = "MotherBoard"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product


class Mouse(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    manufacturer = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    number_of_buttons = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mouse"
        verbose_name_plural = "Mouse"
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption


class Printer(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, null=False, blank=False)
    default = models.BooleanField(default=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    horizontal_resolution = models.IntegerField()
    local = models.BooleanField(default=True)
    name = models.CharField(max_length=250, null=False, blank=False)
    network = models.BooleanField(default=False)
    shared = models.BooleanField(default=False)
    vertical_resolution = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Printer"
        verbose_name_plural = "Printer"
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption


class SoundDevice(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    manufacturer = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    product_name = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SoundDevice"
        verbose_name_plural = "SoundDevice"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product_name


class VideoController(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    adapter_ram = models.IntegerField()
    caption = models.CharField(max_length=250, null=False, blank=False)
    current_bits_per_pixel = models.IntegerField()
    current_horizontal_resolution = models.IntegerField()
    current_number_of_colors = models.IntegerField()
    current_refresh_rate = models.IntegerField()
    current_vertical_resolution = models.IntegerField()
    description = models.CharField(max_length=250, null=False, blank=False)
    driver_date = models.CharField(max_length=250, null=False, blank=False)
    driver_version = models.CharField(max_length=250, null=False, blank=False)
    manufacturer = models.CharField(max_length=250, null=False, blank=False)
    max_refresh_rate = models.IntegerField()
    min_refresh_rate = models.IntegerField()
    name = models.CharField(max_length=250, null=False, blank=False)
    video_mode_description = models.CharField(max_length=250, null=False, blank=False)
    video_processor = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "VideoController"
        verbose_name_plural = "VideoController"
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption


class NetworkAdapter(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    adapter_type = models.CharField(max_length=250, null=False, blank=False)
    caption = models.CharField(max_length=250, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    mac_address = models.CharField(max_length=250, null=False, blank=False)
    manufacturer = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    network_connection_id = models.CharField(max_length=250, null=False, blank=False)
    product_name = models.CharField(max_length=250, null=False, blank=False)
    speed = models.IntegerField()
    bytes_sent_per_sec = models.IntegerField()
    bytes_received_per_sec = models.IntegerField()
    dhcp_server = models.CharField(max_length=250, null=False, blank=False)
    default_ip_gateway_list = models.TextField(null=True, blank=True)
    dns_server_search_order_list = models.TextField(null=True, blank=True)
    ip_address_list = models.TextField(null=True, blank=True)
    ip_subnet_list = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "NetworkAdapter"
        verbose_name_plural = "NetworkAdapter"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product_name


class Memory(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    bank_label = models.CharField(max_length=250, null=False, blank=False)
    capacity = models.IntegerField()
    max_voltage = models.IntegerField()
    min_voltage = models.IntegerField()
    part_number = models.CharField(max_length=250, null=False, blank=False)
    serial_number = models.CharField(max_length=250, null=False, blank=False)
    speed = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Memory"
        verbose_name_plural = "Memory"
        ordering = ["-created_at"]

    def __str__(self):
        return self.bank_label


class CPU(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, null=False, blank=False)
    current_clock_speed = models.IntegerField()
    description = models.CharField(max_length=250, null=False, blank=False)
    max_clock_speed = models.IntegerField()
    name = models.CharField(max_length=250, null=False, blank=False)
    number_of_cores = models.IntegerField()
    number_of_logical_processors = models.IntegerField()
    processor_id = models.CharField(max_length=250, null=False, blank=False)
    socket_designation = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CPU"
        verbose_name_plural = "CPU"
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption


class Core(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False, blank=False)
    percent_processor_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Core"
        verbose_name_plural = "Core"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Keyboard(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    number_of_function_keys = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Keyboard"
        verbose_name_plural = "Keyboard"
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption


class Disk(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    firmware_revision = models.CharField(max_length=250, null=False, blank=False)
    index = models.IntegerField()
    model = models.CharField(max_length=250, null=False, blank=False)
    partitions = models.IntegerField()
    size = models.IntegerField()
    serial_number = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Disk"
        verbose_name_plural = "Disk"
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption


class Partition(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)
    bootable = models.BooleanField(default=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    size = models.IntegerField()
    index = models.IntegerField()
    starting_offset = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Partition"
        verbose_name_plural = "Partition"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Volume(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    partition = models.ForeignKey(Partition, on_delete=models.CASCADE)
    caption = models.CharField(max_length=250, null=False, blank=False)
    file_system = models.CharField(max_length=250, null=False, blank=False)
    free_space = models.IntegerField()
    name = models.CharField(max_length=250, null=False, blank=False)
    size = models.IntegerField()
    volume_serial_number = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Volume"
        verbose_name_plural = "Volume"
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption


class System(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    build_number = models.CharField(max_length=250, null=False, blank=False)
    caption = models.CharField(max_length=250, null=False, blank=False)
    cs_name = models.CharField(max_length=250, null=False, blank=False)
    country_code = models.CharField(max_length=250, null=False, blank=False)
    current_timezone = models.IntegerField()
    install_date = models.CharField(max_length=250, null=False, blank=False)
    last_boot_up = models.CharField(max_length=250, null=False, blank=False)
    os_architecture = models.CharField(max_length=250, null=False, blank=False)
    os_language = models.IntegerField()
    registered_user = models.CharField(max_length=250, null=False, blank=False)
    serial_number = models.CharField(max_length=250, null=False, blank=False)
    status = models.BooleanField(default=True)
    version = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "System"
        verbose_name_plural = "System"
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption


class CPUSensor(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False, blank=False)
    value = models.FloatField(null=False, blank=False, default=0.0)
    sensor_type = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CPUSensor"
        verbose_name_plural = "CPUSensor"
        ordering = ["-created_at"]


class MemorySensor(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False, blank=False)
    value = models.FloatField(null=False, blank=False, default=0.0)
    sensor_type = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "MemorySensor"
        verbose_name_plural = "MemorySensor"
        ordering = ["-created_at"]


class GPUSensor(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False, blank=False)
    value = models.FloatField(null=False, blank=False, default=0.0)
    sensor_type = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "GPUSensor"
        verbose_name_plural = "GPUSensor"
        ordering = ["-created_at"]


class StorageSensor(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False, blank=False)
    value = models.FloatField(null=False, blank=False, default=0.0)
    sensor_type = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "StorageSensor"
        verbose_name_plural = "StorageSensor"
        ordering = ["-created_at"]
