from django.contrib import admin
from attendance.models import *

# Register your models here.

admin.site.register(AttendanceDate)
admin.site.register(AttendanceStudent)
admin.site.register(TeacherAttendanceDate)
admin.site.register(AttendanceTeacher)
