from django.db import models
from django.utils import timezone

# Create your models here.



class ShortLink(models.Model):
    short_url = models.CharField(max_length=255)
    original_url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.original_url

    
    def short_url_exists(self, url):
        return self.objects.filter(short_url=url).exists()
    


class ShortLinkStatistics(models.Model):
    short_url = models.ForeignKey(to=ShortLink, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    ip = models.CharField(max_length=255)
    referrer_url = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return '{} Statistics'.format(self.short_url.short_url)