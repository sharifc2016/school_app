from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^list/', SubjectList.as_view(), name='subject-list'),
    url(r'^add/', AddSubject.as_view(), name='add-subject'),
    url(r'^edit/(?P<id>\d+)/', EditSubject.as_view(), name='edit-subject'),
    url(r'^delete-subject', DeleteSubject.as_view(), name='delete-subject'),
]
