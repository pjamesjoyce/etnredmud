from django.contrib import admin
from content.models import Content, Link
# Register your models here.

class ContentAdmin(admin.ModelAdmin):
    fieldsets=(
        (None, {
            'fields': ('name', 'title', 'body'),
        }),
        ('Links', {
            'classes':('collapse',),
            'fields': ('link1', 'link2', 'link3', 'link4', 'link5')
        })
    )


admin.site.register(Content, ContentAdmin)
admin.site.register(Link)
