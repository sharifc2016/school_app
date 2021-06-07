from django.conf.urls import url
from attendance.views import *

urlpatterns = [
    url(r'^$', AttendanceView.as_view(), name='attendance'),
    url(r'^student-attendance/(?P<id>\d+)/', Attendance.as_view(), name='student-attendance'),
    url(r'^select-level/', SelectAttendanceLevel.as_view(), name='select-level'),
    url(r'^list/(?P<id>\d+)/(?P<date>\d{2}-\d{2}-\d{4})/$', AttendanceList.as_view(), name='attendance-list'),
    url(r'^edit/(?P<id>\d+)/(?P<date>\d{2}-\d{2}-\d{4})/$', EditAttendance.as_view(), name='edit-attendance'),
    # url(r'^delete/(?P<id>\d+)/(?P<date>\d{2}-\d{2}-\d{4})/$', DeteteAttendance.as_view(), name='delete-attendance'),

    # attendance teacher

    url(r'^teacher/$', TeacherAttendanceDateView.as_view(), name='teacher-attendance'),
    url(r'^teacher-attendance/(?P<id>\d+)/', TeacherAttendanceView.as_view(), name='teacher-attendance'),
    url(r'^select-date/', SelectAttendanceDateView.as_view(), name='select-date'),
    url(r'^teacher-absent-list/(?P<date>\d{2}-\d{2}-\d{4})/$', TeacherAttendanceListView.as_view(),
        name='teacher-attendance-list'),
    url(r'^teacher-attendance-edit/(?P<id>\d+)/$', TeacherAttendanceEditView.as_view(),
        name='edit-attendance'),
    # # url(r'^delete/(?P<id>\d+)/(?P<date>\d{2}-\d{2}-\d{4})/$', DeteteAttendance.as_view(), name='delete-attendance'),

]
