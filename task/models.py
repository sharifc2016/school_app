from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from level.models import Level
from subject.models import Subject


# Create your models here.


class TaskInfo(models.Model):
    level = models.ForeignKey(Level, verbose_name='level')
    date = models.DateField(verbose_name='Date')
    image_url = models.TextField(validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.level:
            raise ValidationError(""" Please Select Level """)
        elif not self.date:
            raise ValidationError(""" Please Enter A Valid Date """)
        elif not self.image_url:
            raise ValidationError(""" Please Enter A Valid URL """)

    def __str__(self):
        return str(self.level)


class Task(models.Model):
    info = models.ForeignKey(TaskInfo, verbose_name='task info')
    period = models.IntegerField(verbose_name='Period', null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, blank=True)
    classwork = models.TextField(verbose_name='Class Work', null=True, blank=True)
    homework = models.TextField(verbose_name='Home Work', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.info)
