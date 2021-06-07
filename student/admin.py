from django.contrib import admin
from student.models import Student

class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_display = ['student_id', 'full_name']

admin.site.register(Student, StudentAdmin)
