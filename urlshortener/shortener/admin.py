from django.contrib import admin
from .models import ShortLink, ShortLinkStatistics
# Register your models here.


class ShortLinkStatisticsInline(admin.TabularInline):
    model = ShortLinkStatistics
    fields = ("time", "ip", "referrer_url")
    readonly_fields = ("time", "ip", "referrer_url")


    def has_add_permission(self, request, obj=None):
        return False



class ShortLinkAdmin(admin.ModelAdmin):
    fields = ('short_url', 'original_url', 'is_active', 'expiration_time')
    readonly_fields = ('short_url', 'original_url')
    list_display = ('original_url', 'short_url', 'is_active')
    inlines = (ShortLinkStatisticsInline,)

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(ShortLink, ShortLinkAdmin)
