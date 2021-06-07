from django.conf.urls import url
from student.views import StudentListView, StudentSendSmsView, EditStudent, StudentDetail, StudentDelete, \
    NewStudentView, StudentProfile, Error, StudentTaskList, AllStudentSmsView, GetFullList

# from task.views import TaskList

urlpatterns = [
    # All student list
    url(r'^$', StudentListView.as_view(), name='daseboard'),
    url(r'^list/$', StudentListView.as_view(), name='student_list'),

    # Student details
    url(r'^(?P<student_id>\d+)/details/$', StudentDetail.as_view(), name='student_detail'),

    # Add student
    url(r'^add/$', NewStudentView.as_view(), name='new'),

    # Update student detail
    url(r'^(?P<student_id>\d+)/update/$', EditStudent.as_view(), name='student_edit'),

    # Delete student
    url(r'^(?P<student_id>\d+)/delete/$', StudentDelete.as_view(), name='student_delete'),

    # Student Profile
    url(r'^sprofile/$', StudentProfile.as_view(), name='sprofile'),
    # Task list
    url(r'^task-list/(?P<date>\d{2}-\d{2}-\d{4})/$', StudentTaskList.as_view(), name='list-task'),

    # Task error
    url(r'^error/', Error.as_view(), name='task-error'),
    url(r'^send_sms/(?P<id>\d+)/$', StudentSendSmsView.as_view(), name='student-send-sms'),
    url(r'^all-student-sms-send/$', AllStudentSmsView.as_view(), name='all-student-send-sms'),
    url(r'^student-full-list/$', GetFullList.as_view(), name='get_full_list'),
]
