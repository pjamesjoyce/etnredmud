from django.contrib import admin
from importData.models import DataImport


class DataImportAdmin(admin.ModelAdmin):
    pass

admin.site.register(DataImport, DataImportAdmin)

# Register your models here.
