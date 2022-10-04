from django.contrib import admin
from .models import ShortLink
# Register your models here.


class ShortLinkAdmin(admin.ModelAdmin):
    fields = ('short_url', 'original_url', 'is_active')
    readonly_fields = ('short_url', 'original_url')
    list_display = ('original_url', 'short_url', 'is_active')


    def has_add_permission(self, request, obj=None):
        return False

        
admin.site.register(ShortLink, ShortLinkAdmin)
