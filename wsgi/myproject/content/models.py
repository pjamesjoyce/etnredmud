from django.db import models

# Create your models here.

class Link(models.Model):
    target = models.CharField(max_length=200)
    href = models.CharField(max_length=200)
    alt = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.target

class Content(models.Model):
    class Meta:
        verbose_name = 'Site content'
        verbose_name_plural = 'Site content'

    name = models.CharField(max_length=50)
    title = models.CharField(max_length=255, null = True, blank = True)
    body = models.TextField(null=True, blank=True)
    link1 = models.ForeignKey(Link, null=True, blank=True, related_name='link1')
    link2 = models.ForeignKey(Link, null=True, blank=True, related_name='link2')
    link3 = models.ForeignKey(Link, null=True, blank=True, related_name='link3')
    link4 = models.ForeignKey(Link, null=True, blank=True, related_name='link4')
    link5 = models.ForeignKey(Link, null=True, blank=True, related_name='link5')

    def __unicode__(self):
        return self.name
