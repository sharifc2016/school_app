from django.contrib.auth.models import User

from student.models import Student


def gen():
    students = Student.objects.all()
    for student in students:
        if student.student_level:
            if not student.user:
                roll = str(student.student_id)
                username = student.student_level.institute_name.short_name + str(roll)
                password = "student" + '2017'
                user, created = User.objects.get_or_create(username=username)
                user.set_password(password)
                user.save()
                student.user = user
                student.save()
        else:
            print('No level:',student.full_name)