from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ComputerRawData
from .tasks import parse_computer_raw_data


@receiver(post_save, sender=ComputerRawData)
def trigger_parse_computer_raw_data(sender, instance, created, **kwargs):
    if created:
        parse_computer_raw_data(instance.id)
