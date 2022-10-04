from .models import ShortLink
from django.utils import timezone


def deactivate_expired_shortlinks():
    shortlink_list = ShortLink.objects.all()

    for shortlink in shortlink_list:
        if shortlink.expiration_time is not None:
            if shortlink.expiration_time <= timezone.now():
                shortlink.deactivate()



deactivate_expired_shortlinks()