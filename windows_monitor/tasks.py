from windows_monitor.models import ComputerRawData, Memory, CPU, Core, System
import json
from windows_monitor.models import (
    Computer,
    Bios,
    Monitor,
    MotherBoard,
    Mouse,
    Printer,
    SoundDevice,
    Keyboard,
    Volume,
    VideoController,
    Disk,
    NetworkAdapter,
    Partition,
    CPUSensor,
    StorageSensor,
    MemorySensor,
    GPUSensor
)


def parse_computer_raw_data(id: int):
    obj = ComputerRawData.objects.get(id=id)

    data_systems = json.loads(obj.data_system)
    data_system_2 = json.loads(obj.data_system_2)
    data_bios = json.loads(obj.data_bios)
    sensor_data = json.loads(obj.sensor_data)

    computer = Computer.objects.create(system_uuid=obj.system_uuid)

    for cpu_data in sensor_data.get("Cpu", []):
        CPUSensor.objects.create(
            computer=computer,
            name=cpu_data["Name"],
            value=cpu_data["Value"],
            sensor_type=cpu_data["SensorType"]
        )

    for key, gpu_data_list in sensor_data.items():
        if "Gpu" in key:
            for gpu_data in gpu_data_list:
                GPUSensor.objects.create(
                    computer=computer,
                    name=gpu_data["Name"],
                    value=gpu_data["Value"],
                    sensor_type=gpu_data["SensorType"]
                )

    for memory_data in sensor_data.get("Memory", []):
        MemorySensor.objects.create(
            computer=computer,
            name=memory_data["Name"],
            value=memory_data["Value"],
            sensor_type=memory_data["SensorType"]
        )

    for storage_data in sensor_data.get("Storage", []):
        StorageSensor.objects.create(
            computer=computer,
            name=storage_data["Name"],
            value=storage_data["Value"],
            sensor_type=storage_data["SensorType"]
        )

    for data_system in data_systems:
        system = System.objects.create(
            computer=computer,
            build_number=data_system.get("BuildNumber"),
            caption=data_system.get("Caption"),
            cs_name=data_system.get("CSName"),
            country_code=data_system.get("CountryCode"),
            current_timezone=data_system.get("CurrentTimeZone"),
            install_date=data_system.get("InstallDate"),
            last_boot_up=data_system.get("LastBootUpTime"),
            os_architecture=data_system.get("OSArchitecture"),
            os_language=data_system.get("OSLanguage"),
            registered_user=data_system.get("RegisteredUser"),
            serial_number=data_system.get("SerialNumber"),
            status=True if data_system.get("Status") == "OK" else False,
            version=data_system.get("Version"),
        )
        system.save()

    for data in data_bios:
        bios = Bios.objects.create(
            computer=computer,
            version=data.get("Version"),
            target_os=data.get("TargetOperatingSystem"),
            minor_version=data.get("SystemBiosMinorVersion"),
            major_version=data.get("SystemBiosMajorVersion"),
            status=True if data.get("Status") == "OK" else False,
            name=data.get("Name"),
            manufacturer=data.get("Manufacturer"),
        )
        bios.save()

    monitor_list = data_system_2.get("MonitorList", [])
    for data in monitor_list:
        monitor = Monitor.objects.create(
            computer=computer,
            caption=data.get("Caption"),
            description=data.get("Description"),
            monitor_type=data.get("MonitorType"),
            name=data.get("Name"),
            pixel_x_inch=data.get("PixelsPerXLogicalInch"),
            pixel_y_inch=data.get("PixelsPerYLogicalInch"),
            active=data.get("Active"),
            manufacturer=data.get("ManufacturerName"),
            product_code=data.get("ProductCodeID"),
            serial_number=data.get("SerialNumberID"),
            user_friendly_name=data.get("UserFriendlyName"),
            week_of_manufacture=data.get("WeekOfManufacture"),
            year_of_manufacture=data.get("YearOfManufacture"),
        )
        monitor.save()

    mother_board_list = data_system_2.get("MotherboardList", [])
    for data in mother_board_list:
        mother_board = MotherBoard.objects.create(
            computer=computer,
            manufacturer=data.get("Manufacturer"),
            product=data.get("Product"),
            serial_number=data.get("SerialNumber"),
        )
        mother_board.save()

    mouse_list = data_system_2.get("MouseList", [])
    for data in mouse_list:
        mouse = Mouse.objects.create(
            computer=computer,
            caption=data.get("Caption"),
            description=data.get("Description"),
            manufacturer=data.get("Manufacturer"),
            name=data.get("Name"),
            number_of_buttons=data.get("NumberOfButtons"),
        )
        mouse.save()

    printer_list = data_system_2.get("PrinterList", [])
    for data in printer_list:
        printer = Printer.objects.create(
            computer=computer,
            caption=data.get("Caption"),
            default=data.get("Default"),
            description=data.get("Description"),
            horizontal_resolution=data.get("HorizontalResolution"),
            local=data.get("Local"),
            name=data.get("Name"),
            network=data.get("Network"),
            shared=data.get("Shared"),
            vertical_resolution=data.get("VerticalResolution"),
        )
        printer.save()

    sound_device_list = data_system_2.get("SoundDeviceList", [])
    for data in sound_device_list:
        sound_device = SoundDevice.objects.create(
            computer=computer,
            caption=data.get("Caption"),
            description=data.get("Description"),
            manufacturer=data.get("Manufacturer"),
            name=data.get("Name"),
            product_name=data.get("ProductName"),
        )
        sound_device.save()

    video_controller_list = data_system_2.get("VideoControllerList", [])
    for data in video_controller_list:
        video_controller = VideoController.objects.create(
            computer=computer,
            adapter_ram=data.get("AdapterRAM"),
            caption=data.get("Caption"),
            current_bits_per_pixel=data.get("CurrentBitsPerPixel"),
            current_horizontal_resolution=data.get("CurrentHorizontalResolution"),
            current_number_of_colors=data.get("CurrentNumberOfColors"),
            current_refresh_rate=data.get("CurrentRefreshRate"),
            current_vertical_resolution=data.get("CurrentVerticalResolution"),
            description=data.get("Description"),
            driver_date=data.get("DriverDate"),
            driver_version=data.get("DriverVersion"),
            manufacturer=data.get("Manufacturer"),
            max_refresh_rate=data.get("MaxRefreshRate"),
            min_refresh_rate=data.get("MinRefreshRate"),
            name=data.get("Name"),
            video_mode_description=data.get("VideoModeDescription"),
            video_processor=data.get("VideoProcessor"),
        )
        video_controller.save()

    network_adapter_list = data_system_2.get("NetworkAdapterList", [])
    for data in network_adapter_list:
        network_adapter = NetworkAdapter.objects.create(
            computer=computer,
            adapter_type=data.get("AdapterType"),
            caption=data.get("Caption"),
            description=data.get("Description"),
            mac_address=data.get("MACAddress"),
            manufacturer=data.get("Manufacturer"),
            name=data.get("Name"),
            network_connection_id=data.get("NetConnectionID"),
            product_name=data.get("ProductName"),
            speed=data.get("Speed"),
            bytes_sent_per_sec=data.get("BytesSentPersec"),
            bytes_received_per_sec=data.get("BytesReceivedPersec"),
            dhcp_server=data.get("DHCPServer"),
            default_ip_gateway_list=data.get("DefaultIPGateway"),
            dns_server_search_order_list=data.get("DNSServerSearchOrderList"),
            ip_address_list=data.get("IPAddress"),
            ip_subnet_list=data.get("IPSubnet"),
        )
        network_adapter.save()

    memory_list = data_system_2.get("MemoryList", [])
    for data in memory_list:
        memory = Memory.objects.create(
            computer=computer,
            bank_label=data.get("BankLabel"),
            capacity=data.get("Capacity"),
            max_voltage=data.get("MaxVoltage"),
            min_voltage=data.get("MinVoltage"),
            part_number=data.get("PartNumber"),
            serial_number=data.get("SerialNumber"),
            speed=data.get("Speed"),
        )
        memory.save()

    cpu_list = data_system_2.get("CpuList", [])
    for data in cpu_list:
        cpu = CPU.objects.create(
            computer=computer,
            caption=data.get("Caption"),
            current_clock_speed=data.get("CurrentClockSpeed"),
            description=data.get("Description"),
            max_clock_speed=data.get("MaxClockSpeed"),
            name=data.get("Name"),
            number_of_cores=data.get("NumberOfCores"),
            number_of_logical_processors=data.get("NumberOfLogicalProcessors"),
            processor_id=data.get("ProcessorId"),
            socket_designation=data.get("SocketDesignation"),
        )

        cpu.save()

        cpu_core_list = data.get("CpuCoreList", [])

        for core_data in cpu_core_list:
            core = Core.objects.create(
                computer=computer,
                cpu=cpu,
                name=core_data.get("Name"),
                percent_processor_time=core_data.get("PercentProcessorTime"),
            )
            core.save()

    keyboard_list = data_system_2.get("KeyboardList", [])
    for data in keyboard_list:
        keyboard = Keyboard.objects.create(
            computer=computer,
            caption=data.get("Caption"),
            description=data.get("Description"),
            name=data.get("Name"),
            number_of_function_keys=data.get("NumberOfFunctionKeys"),
        )
        keyboard.save()

    drive_list = data_system_2.get("DriveList", [])
    for data in drive_list:
        disk = Disk.objects.create(
            computer=computer,
            caption=data.get("Caption"),
            description=data.get("Description"),
            firmware_revision=data.get("FirmwareRevision"),
            index=data.get("Index"),
            model=data.get("Model"),
            partitions=data.get("Partitions"),
            size=data.get("Size"),
            serial_number=data.get("SerialNumber"),
        )

        disk.save()

        partition_list = data.get("PartitionList", [])
        for partition_data in partition_list:
            partition = Partition.objects.create(
                computer=computer,
                disk=disk,
                bootable=partition_data.get("Bootable"),
                name=partition_data.get("Name"),
                size=partition_data.get("Size"),
                starting_offset=partition_data.get("StartingOffset"),
                index=partition_data.get("Index"),
            )
            partition.save()

            volume_list = partition_data.get("VolumeList", [])
            for volume_data in volume_list:
                volume = Volume.objects.create(
                    computer=computer,
                    partition=partition,
                    caption=volume_data.get("Caption"),
                    file_system=volume_data.get("FileSystem"),
                    free_space=volume_data.get("FreeSpace"),
                    name=volume_data.get("Name"),
                    size=volume_data.get("Size"),
                    volume_serial_number=volume_data.get("VolumeSerialNumber"),
                )
                volume.save()
