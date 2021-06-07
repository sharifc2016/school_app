from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^list', LevelList.as_view(), name='level-list'),
    url(r'^add', AddLevel.as_view(), name='add-level'),
    url(r'^delete-level', DeleteLevel.as_view(), name='delete-Level'),
    url(r'^edit/(?P<id>\d+)', EditLevel.as_view(), name='edit-Level'),
    url(r'^send-sms/(?P<id>\d+)', LevelSmsView.as_view(), name='sms-Level'),
    url(r'^migrations/$', MigrationsLevelView.as_view(), name='migrations-level'),
    url(r'^migrations/(?P<id>\d+)/$', StudentMigrationView.as_view(), name='migrations-student'),
]
