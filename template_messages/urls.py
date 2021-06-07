from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^add', AddMessage.as_view(), name='sms'),
    url(r'^$', MessageList.as_view(), name='sms-list'),
    url(r'^edit/(?P<id>\d+)', EditMessage.as_view(), name='edit-sms'),
    url(r'^delete/', DeleteMessage.as_view(), name='delete-sms'),
]
