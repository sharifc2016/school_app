from django.db import models

from institute.models import Institute
from level.models import Level
from student.models import Student
from teacher.models import Teacher


class AttendanceDate(models.Model):
    level_name = models.ForeignKey(Level, verbose_name='Level')
    date = models.DateField(verbose_name='Date')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.level_name.name) + ' ' + str(self.date)


class AttendanceStudent(models.Model):
    attendance_date = models.ForeignKey(AttendanceDate, verbose_name='Attendance Date')
    student_name = models.ForeignKey(Student, verbose_name='Student')
    attendance = models.BooleanField(default=True)

    def __str__(self):
        return str(self.attendance_date.date) + ' ' + str(self.student_name.full_name)


class TeacherAttendanceDate(models.Model):
    institute = models.ForeignKey(Institute, verbose_name="Institute")
    date = models.DateField(verbose_name='Date')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.institute.name) + ' ' + str(self.date)


class AttendanceTeacher(models.Model):
    attendance_date = models.ForeignKey(TeacherAttendanceDate, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, null=True, blank=True)
    attendance = models.BooleanField(default=True)

    def __str__(self):
        return str(self.teacher)
