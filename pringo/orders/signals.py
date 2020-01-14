from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Order
from .utils import unidecode_string


@receiver(pre_save, sender=Order)
def decode_customer_name(sender, instance, **kwargs):
    instance.customer_name = instance.customer_name.title()
    instance.customer_name_decoded = unidecode_string(instance.customer_name)
