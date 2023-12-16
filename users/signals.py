from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import BearerTokenAuthentication


@receiver(pre_save, sender=BearerTokenAuthentication)
def set_token_expiration(sender, instance=None, **kwargs):
    if instance and not instance.ttl:
        instance.ttl = timezone.now() + timezone.timedelta(minutes=1)
