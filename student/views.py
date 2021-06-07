from mailbox import Message

from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.urls.base import reverse
from institute.models import Institute
from django.views.generic import View
from django.shortcuts import redirect
from student.models import Student
from django.contrib.auth.models import User
from task.models import Task
from task.models import TaskInfo
import datetime
from student.forms import StudentAddForm
from template_messages.views import send_sms
from template_messages.models import Message
import pprint


# Student list
class StudentListView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('sprofile'))

        template_name = 'student/list.html'
        students = Student.objects.filter(student_level__institute_name=institutes[0])
        context = {
            'students': students,
            'message': Message.objects.filter(institute=institutes[0].id)
        }

        return render(request, template_name, context)


# Student detail
class StudentDetail(View):

    def get(self, request, student_id):

        # User authentication
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect('sprofile')

        student = get_object_or_404(Student, pk=student_id)
        template_name = 'student/detail.html'
        context = {'student': student}
        return render(request, template_name, context)

    def post(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        template_name = 'student/detail.html'

        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        username = 'dpsc' + str(student.student_id)
        if pass1 == pass2:
            user = User.objects.get(username=username)
            user.set_password(pass2)
            user.save()
            context = {
                'student': student,
                'password1': "Password Changed Succesfully"
            }
        else:
            context = {
                'student': student,
                'password': "Password not matched"
            }
        return render(request, template_name, context)


# Add student
class NewStudentView(View):

    def get(self, request):
        # User authentication
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect('sprofile')

        form = StudentAddForm(institute=institutes[0].id)
        return render(request, 'student/add.html', {'form': form})

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect('sprofile')
        form = StudentAddForm(institutes[0].id, request.POST, request.FILES)
        users = User.objects.all()
        student_id = form['student_id'].value()
        institute = Institute.objects.get(user = request.user)
        short_name = institute.short_name
        for user in users:
            if user.username == str(short_name) + student_id:
                error_message = 'This student_id is already exist!'
                return render(request, 'student/add.html', {'form': form, 'error_message': error_message})

        if form.is_valid():
            student = form.save(commit=False)
            roll = form['student_id'].value()
            username = str(short_name) + str(roll)
            password = "student" + '2017'
            user = User.objects.create_user(username=username, password=password)
            user.save()
            student.user = user
            student.save()
            return HttpResponseRedirect(reverse('student_list'))


# Edit student
class EditStudent(View):

    def get(self, request, student_id):
        # User authentication
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect('sprofile')

        student = get_object_or_404(Student, pk=student_id)
        form = StudentAddForm(institutes[0].id, instance=student)
        return render(request, 'student/edit.html', {'form': form})

    def post(self, request, student_id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect('sprofile')
        student = get_object_or_404(Student, pk=student_id)
        form = StudentAddForm(institutes[0].id, request.POST, request.FILES, instance=student)
        institute = Institute.objects.get(user = request.user)
        short_name = institute.short_name
        if form.is_valid():
            form = form.save(commit=False)
            # date = student.admission_year
            # +student.admission_year = datetime.datetime.strptime(str(date), '%Y/%d/%m').strftime('%d-%m-%Y')
            form.save()
            user = student.user
            user.username = str(short_name) + str(form.student_id)
            user.save()
            student.save()
            return redirect('student_list')

        return render(request, 'student/edit.html', {'form': form})


# Student delete
class StudentDelete(View):

    def get(self, request, student_id):
        # User authentication
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect('sprofile')
        student = Student.objects.get(id=student_id)
        user = student.user
        user.delete()
        return redirect('student_list')


# Student Userprofile
class StudentProfile(View):
    template_name = 'student/task_list_1.html'
    template_name_2 = 'student/task_view.html'
    context = {}

    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if institutes:
            return HttpResponseRedirect(reverse('student_list'))
        user = request.user
        student_id = user.username[4:]
        # student = Student.objects.get(student_id = student_id)

        self.context['now'] = datetime.datetime.now().strftime("%d-%m-%Y")

        return render(request, self.template_name, self.context)

    def post(self, request):
        template_name_2 = 'student/task_view.html'
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if institutes:
            return HttpResponseRedirect(reverse('student_list'))

        user = request.user
        student_id = user.username[4:]
        student = Student.objects.get(student_id=student_id)

        level = student.student_level
        date = request.POST['date']
        date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
        t = TaskInfo.objects.all()
        for i in t:
            if str(i.date) == date and i.level == level:
                task = TaskInfo.objects.get(date=date, level=level)
                context = {
                    'image_url': task.image_url
                }
                return render(request, template_name_2, context)
        else:
            return HttpResponseRedirect(reverse('task-error'))


# Task list by class and date.
class StudentTaskList(View):
    template_name = 'student/task_list.html'
    context = {}

    def get(self, request, date):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if institutes:
            return HttpResponseRedirect(reverse('student_list'))

        date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
        t = TaskInfo.objects.all()
        user = request.user
        student_id = user.username[4:]
        student = Student.objects.get(student_id=student_id)
        level = student.student_level_id
        for i in t:
            if str(i.date) == date and str(i.level_id) == str(level):
                id = i.level
                t = Task.objects.filter(info__date=date, info__level=level)
                if not t:
                    return HttpResponseRedirect(reverse('task-error'))
                self.context['task'] = Task.objects.filter(info__date=date, info__level=level)
                self.context['date'] = date
                self.context['id'] = id
                return render(request, self.template_name, self.context)
        else:
            return HttpResponseRedirect(reverse('task-error'))


# If no task will available then task error
class Error(View):
    template_name = 'student/error.html'

    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if institutes:
            return HttpResponseRedirect(reverse('student_list'))

        return render(request, self.template_name)


class StudentSendSmsView(View):
    def get(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('student_list'))

        template_name = 'student/student_sms.html'
        context = {
            'student': Student.objects.get(id=id)
        }
        return render(request, template_name, context)

    def post(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('student_list'))

        stduent = Student.objects.get(id=id)
        contact_number = stduent.contact
        message = request.POST['msg']
        note = "To contacts " + ','.join(contact_number)
        institute = Institute.objects.get(user=request.user)
        api_key = institute.sms_api_key
        username = institute.sms_username
        success = 0
        level = stduent.student_level
        name = stduent.full_name
        roll = stduent.student_id
        std_sms = message.format(c=level, n=name, r=roll)
        result = send_sms(std_sms, note, [stduent.contact], api_key, username)
        success += int(result['success'])

        template_name = 'student/list.html'
        students = Student.objects.filter(student_level__institute_name=institutes[0])
        context = {
            'students': students,
            'success': "{} message(s) send successfully.".format(success),
        }
        return render(request, template_name, context)


class AllStudentSmsView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('student_list'))

        template_name = 'student/all-student-sms.html'
        get_students = Student.objects.filter(student_level__institute_name=institutes[0].id)
        total_student = len(get_students)
        context = {
            'total_student' : total_student,
            'message': Message.objects.filter(institute=institutes[0]),
        }
        return render(request, template_name, context)

    def post(self, request):
        template_name = 'student/all-student-sms.html'
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        get_students = Student.objects.filter(student_level__institute_name=institutes[0])
        if len(get_students) == 0:
            template_name = 'student/all-student-sms.html'
            context = {
                'total_student': len(get_students),
                'error_message': "There is no student to this level, Please add student first."
            }
            return render(request, template_name, context)
        student = []
        for s in get_students:
            student += [s.id]
        success = 0
        for i in range(0, len(student), 100):
            stds = student[i:i + 100]
            ss = [int(s) for s in stds]
            students = Student.objects.filter(id__in=ss)
            contacts = [s.contact for s in students]
            message = request.POST['msg']
            note = "To contacts " + ','.join(contacts)
            institute = Institute.objects.get(user=request.user)
            api_key = institute.sms_api_key
            username = institute.sms_username

            for s in students:
                level = s.student_level
                name = s.full_name
                roll = s.student_id
                std_sms = message.format(c=level, n=name, r=roll)
                result = send_sms(std_sms, note, [s.contact], api_key, username)
                success += int(result['success'])

        student = Student.objects.filter(student_level__institute_name=institutes[0])
        if student:
            context = {
                'total_student': len(student),
                'message': Message.objects.filter(institute=institutes[0]),
                'success': "{} message send successfully.".format(success)
            }
            return render(request, template_name, context)
        else:
            return redirect('student-list')


class GetFullList(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('sprofile'))

        template_name = 'student/get_all_student_list.html'
        students = Student.objects.filter(student_level__institute_name=institutes[0])
        context = {
            'students': students,
            'message': Message.objects.filter(institute=institutes[0].id)
        }

        return render(request, template_name, context)
