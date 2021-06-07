from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Institute(models.Model):
    name = models.CharField(verbose_name='Institute Name', max_length=250)
    address = models.TextField(verbose_name='Address')
    phone = models.CharField(verbose_name='Phone', max_length=15)
    email = models.CharField(verbose_name='Email', max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='User', null=True, blank=True)
    sms_api_key = models.CharField(max_length= 100, blank=True, null=True)
    sms_username = models.CharField(max_length= 50, blank= True, null= True)
    short_name = models.CharField(max_length=20, default='ITSD')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
