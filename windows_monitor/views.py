from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from windows_monitor.serializers import ComputerRawDataInputSerializer
from windows_monitor.services import ComputerDataService
from django.shortcuts import render
from django.db.models import Max, Prefetch
from windows_monitor.models import (
    Computer,
    Bios,
    Monitor,
    MotherBoard,
    Mouse,
    Printer,
    SoundDevice,
    VideoController,
    NetworkAdapter,
    Memory,
    CPU,
    Core,
    Keyboard,
    Disk,
    Partition,
    Volume,
    System, CPUSensor, MemorySensor, GPUSensor, StorageSensor
)


class ComputerRawDataCreateView(APIView):
    _service = ComputerDataService()

    def post(self, request):
        serializer = ComputerRawDataInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._service.create_computer_data(serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


def computer_list(request):
    unique_computers = Computer.objects.values('system_uuid').annotate(latest_created_at=Max('created_at')).order_by(
        '-latest_created_at')
    return render(request, 'windows_monitor/computer_list.html', {'computers': unique_computers})


def computer_detail(request, system_uuid):
    computers = Computer.objects.filter(system_uuid=system_uuid).order_by('-created_at')
    current_computer = computers.first()

    context = {
        'computer': current_computer,
        'bios': Bios.objects.filter(computer=current_computer).first(),
        'monitors': Monitor.objects.filter(computer=current_computer),
        'motherboard': MotherBoard.objects.filter(computer=current_computer).first(),
        'mouse': Mouse.objects.filter(computer=current_computer).first(),
        'printers': Printer.objects.filter(computer=current_computer),
        'sound_devices': SoundDevice.objects.filter(computer=current_computer),
        'video_controllers': VideoController.objects.filter(computer=current_computer),
        'network_adapters': NetworkAdapter.objects.filter(computer=current_computer),
        'memory_modules': Memory.objects.filter(computer=current_computer),
        'cpus': CPU.objects.filter(computer=current_computer).prefetch_related('core_set'),
        'cores': Core.objects.filter(computer=current_computer),
        'keyboard': Keyboard.objects.filter(computer=current_computer).first(),
        'disks': Disk.objects.filter(computer=current_computer).prefetch_related(
            Prefetch('partition_set', queryset=Partition.objects.prefetch_related('volume_set'))
        ),
        'partitions': Partition.objects.filter(computer=current_computer),
        'volumes': Volume.objects.filter(computer=current_computer),
        'system': System.objects.filter(computer=current_computer).first(),
        'computers': computers,
        'cpu_sensors': CPUSensor.objects.filter(computer=current_computer),
        'memory_sensors': MemorySensor.objects.filter(computer=current_computer),
        'gpu_sensors': GPUSensor.objects.filter(computer=current_computer),
        'storage_sensors': StorageSensor.objects.filter(computer=current_computer),
    }

    return render(request, 'windows_monitor/computer_detail.html', context)
