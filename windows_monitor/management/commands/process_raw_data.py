from django.core.management.base import BaseCommand

from windows_monitor.tasks import parse_computer_raw_data


class Command(BaseCommand):
    help = "Process data from ComputerRawData"

    def handle(self, *args, **options):
        parse_computer_raw_data(7)
