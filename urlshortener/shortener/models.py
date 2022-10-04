from django.db import models

# Create your models here.



class ShortLink(models.Model):
    short_url = models.CharField(max_length=255)
    original_url = models.CharField(max_length=255)


    class Meta:

        def __str__(self):
            return self.short_url

    
    def short_url_exists(self, url):
        return self.objects.filter(short_url=url).exists()