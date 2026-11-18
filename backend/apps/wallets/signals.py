from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Wallet


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet(sender, instance, created, **kwargs):
    """Every account gets its wallet the moment it exists (signup, admin or createsuperuser)."""
    if created:
        Wallet.objects.get_or_create(user=instance)
