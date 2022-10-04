from django.db import models
from django.utils import timezone

# Create your models here.



class ShortLink(models.Model):
    short_url = models.CharField(max_length=255)
    original_url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    expiration_time = models.DateTimeField(default=None, null=True, blank=True)
    max_clicks = models.IntegerField(default=5)
    
    
    def __str__(self):
        return self.original_url

    
    def short_url_exists(self, url):
        return self.objects.filter(short_url=url).exists()
    
    
    @property
    def can_be_opened(self):
        if not self.is_time_expired() and not self.is_max_clicks_exceeded():
            return self.is_active
        return False


    @property
    def clicks_count(self):
        return ShortLinkStatistics.objects.filter(short_url=self).count()


    @property
    def is_expired(self):
        if self.expiration_time is None:
            return False
        return self.expiration_time <= timezone.now()


    def is_time_expired(self):
        if self.is_expired:
            self.deactivate()
            return True
        return False
        

    def is_max_clicks_exceeded(self):
        if self.clicks_count < self.max_clicks:
            return False
        self.deactivate()
        return True

    
    def deactivate(self):
        self.is_active = False
        self.save()



class ShortLinkStatistics(models.Model):
    short_url = models.ForeignKey(to=ShortLink, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    ip = models.CharField(max_length=255)
    referrer_url = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return '{} Statistics'.format(self.short_url.short_url)