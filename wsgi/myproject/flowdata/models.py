from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

UNIT_CHOICES = (
    ('Mass', (
        ('kg', 'kg'),
        ('t', 'tonne'),
    )
    ),
    ('Energy', (
        ('kWh', 'kWh'),
    )
    ),
    ('Volume', (
        ('m3', 'm3'),
    )
    ),
    ('Radioactivity', (
        ('Bq', 'Bq'),
    )
    ),
    ('Time', (
        ('h', 'hours'),
        ('d', 'days'),
    )
    ),
    ('Amount', (
        ('p', 'Item'),
    )
    ),
)


# Create your models here.
class FlowInputSubstance(models.Model):
    class Meta:
        verbose_name = 'Input'
    name = models.CharField(max_length=128)
    emission_factor = models.FloatField()
    unit = models.CharField(max_length=5, choices = UNIT_CHOICES, default='kg')
    simaPro_id = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name + " (" + self.unit +")"

class FlowOutputSubstance(models.Model):
    class Meta:
        verbose_name = 'Output'
    name = models.CharField(max_length=128)
    emission_factor = models.FloatField()
    unit = models.CharField(max_length=5, choices = UNIT_CHOICES, default='kg')
    simaPro_id = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name + " (" + self.unit +")"

class FlowTechnosphere(models.Model):
    class Meta:
        verbose_name = 'Technosphere intermediate'
    name = models.CharField(max_length=128)
    unit = models.CharField(max_length=5, choices = UNIT_CHOICES, default='kg')

    def __unicode__(self):
        return self.name + " (" + self.unit +")"

class FlowSystem(models.Model):
    class Meta:
        verbose_name_plural = 'Systems'

    owner = models.ForeignKey(User)
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    def user_can_edit(self, user):
        return user == self.owner

class FlowTransformation(models.Model):
    class Meta:
        verbose_name_plural = 'Transformation processes'

    name = models.CharField(max_length=128)
    unit = models.CharField(max_length=5, choices = UNIT_CHOICES, default='kg')
    category = models.CharField(max_length=50, default = 'Uncategorized')
    author = models.ForeignKey(User, null = True)
    partOfSystem = models.ManyToManyField(FlowSystem)
    uuid = models.CharField(max_length=36,default=str(uuid.uuid4()))

    inputflows = models.ManyToManyField(FlowInputSubstance, through = 'FlowInputMembership')
    outputflows = models.ManyToManyField(FlowOutputSubstance, through = 'FlowOutputMembership')
    technosphereInputs = models.ManyToManyField(FlowTechnosphere, related_name='techInputs', through = 'FlowTechnosphereMembershipInput')
    technosphereOutputs = models.ManyToManyField(FlowTechnosphere, related_name='techOutputs', through = 'FlowTechnosphereMembershipOutput')


    def __unicode__(self):
        return "%s. %s (%s)" % (self.id, self.name, self.unit)

# Membership classes for ManyToManyField fields


class FlowInputMembership(models.Model):
    transformation = models.ForeignKey(FlowTransformation, on_delete = models.CASCADE)
    inputsubstance = models.ForeignKey(FlowInputSubstance, on_delete = models.CASCADE, verbose_name='Input')
    amount_required = models.FloatField()
    partOfSystem = models.ForeignKey(FlowSystem, on_delete = models.CASCADE)
    note = models.CharField(max_length = 500, null = True)
    uuid = models.CharField(max_length=36,default=str(uuid.uuid4()))

    def __unicode__(self):
        return "%s : %s -> %s (%s)" % (self.id, self.inputsubstance, self.transformation, self.partOfSystem)

class FlowOutputMembership(models.Model):
    transformation = models.ForeignKey(FlowTransformation, on_delete = models.CASCADE)
    outputsubstance = models.ForeignKey(FlowOutputSubstance, on_delete = models.CASCADE, verbose_name='Output/Emissions')
    amount_required = models.FloatField()
    partOfSystem = models.ForeignKey(FlowSystem, on_delete = models.CASCADE)
    note = models.CharField(max_length = 500, null = True)
    uuid = models.CharField(max_length=36,default=str(uuid.uuid4()))

    def __unicode__(self):
        return "%s : %s -> %s (%s)" % (self.id, self.transformation, self.outputsubstance, self.partOfSystem)

class FlowTechnosphereMembershipInput(models.Model):
    transformation = models.ForeignKey(FlowTransformation, on_delete = models.CASCADE)
    techFlow = models.ForeignKey(FlowTechnosphere, on_delete = models.CASCADE, verbose_name='Input')
    amount_required = models.FloatField()
    partOfSystem = models.ForeignKey(FlowSystem, on_delete = models.CASCADE)
    note = models.CharField(max_length = 500, null = True)
    uuid = models.CharField(max_length=36,default=str(uuid.uuid4()))

    def __unicode__(self):
        return "%s : %s -> %s (%s)" % (self.id, self.techFlow, self.transformation, self.partOfSystem)

class FlowTechnosphereMembershipOutput(models.Model):
    transformation = models.ForeignKey(FlowTransformation, on_delete = models.CASCADE)
    techFlow = models.ForeignKey(FlowTechnosphere, on_delete = models.CASCADE, verbose_name='Output/Emissions')
    amount_required = models.FloatField()
    partOfSystem = models.ForeignKey(FlowSystem, on_delete = models.CASCADE)
    note = models.CharField(max_length = 500, null = True)
    uuid = models.CharField(max_length=36,default=str(uuid.uuid4()))

    def __unicode__(self):
        return "%s : %s -> %s (%s)" % (self.id, self.transformation, self.techFlow, self.partOfSystem)
