from django.contrib import admin
from data.models import InputSubstance, OutputSubstance, Institution, UserProfile, Process, SubProcess, ProcessMembership, InputMembership, OutputMembership
# Register your models here.

admin.site.register(InputSubstance)
admin.site.register(OutputSubstance)
admin.site.register(Institution)
admin.site.register(UserProfile)


class SubProcessInline(admin.StackedInline):
    model = ProcessMembership
    extra = 1

class InputInline(admin.StackedInline):
    model = InputMembership
    extra = 1

class OutputInline(admin.StackedInline):
    model = OutputMembership
    extra = 1


class ProcessAdmin(admin.ModelAdmin):
    exclude = []
    inlines = [SubProcessInline]

class SubProcessAdmin(admin.ModelAdmin):
    exclude = []
    inlines = [InputInline, OutputInline]

admin.site.register(Process,ProcessAdmin)
admin.site.register(SubProcess, SubProcessAdmin)
