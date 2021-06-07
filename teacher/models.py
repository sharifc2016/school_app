from django.contrib.auth.models import User
from django.db import models
# from django.utils.datetime_safe import datetime
from datetime import datetime
from institute.models import Institute


class Teacher(models.Model):
    YEAR_CHOICES = []
    for r in range(1980, (datetime.now().year)+2):
        YEAR_CHOICES.append((r, r))
    institute = models.ForeignKey(Institute, verbose_name="Institute")
    teacher_id = models.IntegerField(verbose_name='Teacher ID', null=True, blank=True)
    join_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.now().year,  null=True, blank=True)
    full_name = models.CharField(max_length=100, verbose_name='Full name',  null=True, blank=True)
    father_name = models.CharField(max_length=100, verbose_name='Father name',  null=True, blank=True)
    mother_name = models.CharField(max_length=100, verbose_name='Mother name', null=True, blank=True)
    dob = models.DateField(verbose_name='Date of birth', null=True, blank=True)
    address = models.TextField(verbose_name='Address', max_length=500, null=True, blank=True)
    contact = models.CharField(verbose_name='Contact', max_length=200, null=True, blank=True)
    image = models.ImageField(default='uploads/images/no-img.jpg', upload_to='uploads/images/', null=True, blank=True)
    extra = models.TextField(verbose_name='Remark', max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.full_name)
