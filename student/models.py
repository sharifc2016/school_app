from django.contrib.auth.models import User
from django.db import models
from level.models import Level
from datetime import datetime


class Student(models.Model):
    YEAR_CHOICES = []
    for r in range(1980, (datetime.now().year + 2)):
        YEAR_CHOICES.append((r, r))

    student_id = models.IntegerField(verbose_name='Student roll', null=True)
    student_level = models.ForeignKey(Level, null=True, blank=True, related_name='Level')
    admission_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.now().year)
    full_name = models.CharField(max_length=100, verbose_name='Full name')
    father_name = models.CharField(max_length=100, verbose_name='Father name')
    mother_name = models.CharField(max_length=100, verbose_name='Mother name')
    dob = models.DateField('Date of birth')
    address = models.TextField(verbose_name='Address', max_length=500)
    contact = models.CharField(verbose_name='Contact', max_length=200)
    image = models.ImageField(default='uploads/images/no-img.jpg', upload_to='uploads/images/')
    extra = models.TextField(verbose_name='Remark', max_length=500)
    user = models.ForeignKey(User,blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


