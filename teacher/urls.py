from django.conf.urls import url
from teacher.views import *

urlpatterns = [
    url(r'^add/', TeacherAdd.as_view(), name="teacher-add"),
    url(r'^edit/(?P<id>\d+)/$', TeacherEdit.as_view(), name="teacher-edit"),
    url(r'^details/(?P<id>\d+)/$', TeacherDetails.as_view(), name="teacher-details"),
    url(r'^delete/', TeacherDelete.as_view(), name="teacher-delete"),
    url(r'^list/', TeacherList.as_view(), name="teacher-list"),
    url(r'^send_sms/(?P<id>\d+)/$', TeacherSendSmsView.as_view(), name='teacher-send-sms'),
    url(r'^all-teacher-sms-send/$', AllTeacherSmsView.as_view(), name='all-teacher-send-sms'),
    # url(r'^teacher/print/(?P<id>\d+)/$', TeacherPrint.as_view(), name='teacher-print'),
]
