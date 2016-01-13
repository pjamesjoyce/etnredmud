from django.contrib import admin
from flowdata.models import FlowSystem, FlowTechnosphere, FlowInputSubstance, FlowTransformation, FlowInputMembership, FlowOutputSubstance, FlowOutputMembership, FlowTechnosphereMembershipInput, FlowTechnosphereMembershipOutput
# Register your models here.

admin.site.register(FlowSystem)
admin.site.register(FlowTechnosphere)
admin.site.register(FlowInputSubstance)
#admin.site.register(FlowTransformation)
admin.site.register(FlowInputMembership)
admin.site.register(FlowOutputSubstance)
admin.site.register(FlowOutputMembership)
admin.site.register(FlowTechnosphereMembershipInput)
admin.site.register(FlowTechnosphereMembershipOutput)


class FlowInputInline(admin.StackedInline):
    model = FlowInputMembership
    extra = 1

class FlowOutputInline(admin.StackedInline):
    model = FlowOutputMembership
    extra = 1

class FlowTechOutputInline(admin.StackedInline):
    model = FlowTechnosphereMembershipOutput
    extra = 1

class FlowTechInputInline(admin.StackedInline):
    model = FlowTechnosphereMembershipInput
    extra = 1

class FlowTransformationAdmin(admin.ModelAdmin):
    exclude = []
    inlines = [FlowInputInline, FlowOutputInline, FlowTechInputInline, FlowTechOutputInline]

admin.site.register(FlowTransformation,FlowTransformationAdmin)
