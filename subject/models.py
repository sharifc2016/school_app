from django.db import models
from level.models import Level


# Create your models here.

class Subject(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50)
    level_name = models.ForeignKey(Level, verbose_name='Level')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
