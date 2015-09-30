from django.db import models
from django.contrib.auth.models import User
from time import time

# Create your models here.

def get_upload_file_name(instance, filename):
    print  "%s_%s" % (str(time()).replace('.','_'), filename)
    return "%s_%s" % (str(time()).replace('.','_'), filename)

def get_default_user():
    return User.objects.get(id=1)


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
class InputSubstance(models.Model):
    class Meta:
        verbose_name = 'Input'
    name = models.CharField(max_length=128)
    emission_factor = models.FloatField()
    unit = models.CharField(max_length=5, choices = UNIT_CHOICES, default='kg')
    simaPro_id = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name + " (" + self.unit +")"

class OutputSubstance(models.Model):
    class Meta:
        verbose_name = 'Output'
    name = models.CharField(max_length=128)
    emission_factor = models.FloatField()
    unit = models.CharField(max_length=5, choices = UNIT_CHOICES, default='kg')
    simaPro_id = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name + " (" + self.unit +")"

class Institution(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    institution = models.ForeignKey(Institution, blank=True, null=True)
    esr_number = models.IntegerField(blank=True, null=True)
    work_package = models.IntegerField(blank=True, null=True)
    profile_picture = models.FileField(upload_to=get_upload_file_name, blank =True)

    def __unicode__(self):
        return self.user.username + " profile data"

    def get_profile_picture(self):
		profile_pic = str(self.profile_picture)
		return profile_pic


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class SubProcess(models.Model):
    class Meta:
        verbose_name_plural = 'Subprocesses'

    name = models.CharField(max_length=128)
    unit = models.CharField(max_length=5, choices = UNIT_CHOICES, default='kg')
    category = models.CharField(max_length=50, default = 'Uncategorized')
    author = models.ForeignKey(User, null = True)
    inputs = models.ManyToManyField(InputSubstance, through = 'InputMembership')
    outputs = models.ManyToManyField(OutputSubstance, through = 'OutputMembership')


    def __unicode__(self):
        return self.name + " (" + self.unit +")"



class Process(models.Model):
    class Meta:
        verbose_name_plural = 'Processes'

    owner = models.ForeignKey(User)
    name = models.CharField(max_length=128)
    output = models.CharField(max_length=128)
    output_amount = models.FloatField()
    unit = models.CharField(max_length=5, choices = UNIT_CHOICES, default='kg')
    subprocesses = models.ManyToManyField(SubProcess, through = 'ProcessMembership')

    def __unicode__(self):
        return self.name

    def user_can_edit(self, user):
        return user == self.owner



# Membership classes for ManyToManyField fields

class ProcessMembership(models.Model):
    subprocess = models.ForeignKey(SubProcess, on_delete = models.CASCADE)
    process = models.ForeignKey(Process, on_delete = models.CASCADE)
    amount_required = models.FloatField()
    note = models.CharField(max_length = 500, null = True)

class InputMembership(models.Model):
    subprocess = models.ForeignKey(SubProcess, on_delete = models.CASCADE)
    inputsubstance = models.ForeignKey(InputSubstance, on_delete = models.CASCADE, verbose_name='Input')
    amount_required = models.FloatField()
    note = models.CharField(max_length = 500, null = True)

class OutputMembership(models.Model):
    subprocess = models.ForeignKey(SubProcess, on_delete = models.CASCADE)
    outputsubstance = models.ForeignKey(OutputSubstance, on_delete = models.CASCADE, verbose_name='Output/Emissions')
    amount_required = models.FloatField()
    note = models.CharField(max_length = 500, null = True)
