from django.conf.urls import url
from task.views import *

urlpatterns = [
    url(r'^add-task/', AddTaskInfo.as_view(), name='add-task-info'),
    # url(r'^add-task/(?P<id>[0-9]+)', AddTask.as_view(), name='add-task'),
    url(r'^list/', SelectLevel.as_view(), name='list-task'),
    url(r'^task-list/$', TaskList.as_view(), name='task_list'),
    url(r'^view/(?P<id>\d+)/$', ViewTask.as_view(), name='view_task'),
    url(r'^error/', Error.as_view(), name='task-error'),
    url(r'^edit/(?P<id>\d+)/$', EditTask.as_view(), name='edit-task'),
    url(r'^delete/$', DeleteTask.as_view(), name='delete-tasks'),
]
