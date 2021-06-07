from django.db import models
from institute.models import Institute


# Create your models here.

class Level(models.Model):
    institute_name = models.ForeignKey(Institute, verbose_name='Institute', null=True, blank=True)
    name = models.CharField(verbose_name='Name', max_length=50)
    room = models.CharField(verbose_name='Room', max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
