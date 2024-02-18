from django.contrib import admin
from .models import Apostila, ViewApostila, Tag


class ApostilaAdmin(admin.ModelAdmin):
    list_display = ['user', 'titulo', 'arquivo', 'tag']

    def tag(self, obj):
        return [tag.tag for tag in obj.tags.all()]


class ViewApostilaAdmin(admin.ModelAdmin):
    list_display = ['ip', 'apostila']
    

admin.site.register(Apostila, ApostilaAdmin)
admin.site.register(ViewApostila, ViewApostilaAdmin)
admin.site.register(Tag)
