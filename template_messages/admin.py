from django.contrib import admin

# Register your models here.
from template_messages.models import Message

admin.site.register(Message)
