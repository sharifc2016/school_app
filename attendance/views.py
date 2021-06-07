import datetime

from django.http.response import HttpResponse

from institute.models import Institute
from student.models import Student
from template_messages.views import send_sms
from template_messages.models import Message
from attendance.forms import *
from attendance.models import *
from datetime import datetime
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.

class AttendanceView(View):
    context = {}
    template_name = 'attendance/attendance.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        else:
            attendance_form = AttendanceDateForm(institute=institutes[0].id)
            form = attendance_form
            self.context['form'] = form
            return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        if 'save' in request.POST.keys():

            form = AttendanceDateForm(institutes[0].id, request.POST)
            attendance_date = AttendanceDate.objects.all()
            date = datetime.strptime(request.POST['date'], '%d-%m-%Y').strftime('%Y-%m-%d')
            level = request.POST['level_name']
            for att in attendance_date:
                if level == str(att.level_name.id) and date == str(att.date):
                    date = request.POST['date']
                    context = {
                        'attendance_level': level,
                        'date': date
                    }
                    return render(request, self.template_name, context)

            if form.is_valid():
                attendance = form.save()
                return HttpResponseRedirect('/attendance/student-attendance/' + str(attendance.id) + '/')


class Attendance(View):
    template_name = 'attendance/list.html'
    context = {}

    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        attendance = AttendanceDate.objects.get(id=id)
        level = attendance.level_name
        student = Student.objects.filter(student_level=level)
        if student:
            self.context['student'] = Student.objects.filter(student_level=level)
            self.context['form'] = AttendanceForm
            self.context['att'] = AttendanceDate.objects.get(id=id)
            self.context['message'] = Message.objects.filter(institute=institutes[0])
            self.context['success'] = None
            return render(request, self.template_name, self.context)
        else:
            return HttpResponseRedirect('/attendance/')

    def post(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        if 'save' in request.POST:
            get_students = request.POST.getlist('student')
            students = [int(s) for s in get_students]
            attendance_date = AttendanceDate.objects.get(id=id)
            level_students = Student.objects.filter(student_level=attendance_date.level_name)

            for student in level_students:
                obj, created = AttendanceStudent.objects.get_or_create(attendance_date=attendance_date,
                                                                       student_name=student)
                if student.id in students:
                    obj.attendance = False
                    obj.save()
                else:
                    obj.attendance = True
                    obj.save()
            return HttpResponseRedirect('/attendance/')

        else:
            get_students = request.POST.getlist('student')
            students = [int(s) for s in get_students]
            attendance_date = AttendanceDate.objects.get(id=id)
            level_students = Student.objects.filter(student_level=attendance_date.level_name)

            for student in level_students:
                obj, created = AttendanceStudent.objects.get_or_create(attendance_date=attendance_date,
                                                                       student_name=student)
                if student.id in students:
                    obj.attendance = False
                    obj.save()
                else:
                    obj.attendance = True
                    obj.save()

            ss = [int(s) for s in get_students]
            stds = Student.objects.filter(id__in=ss)
            contacts = [s.contact for s in stds]
            message = Message.objects.get(id=int(request.POST.get('msg_id', 0)))
            note = "To contacts " + ','.join(contacts)
            institute = Institute.objects.get(user=request.user)
            api_key = institute.sms_api_key
            username = institute.sms_username
            success = 0
            for s in stds:
                level = s.student_level
                name = s.full_name
                roll = s.student_id
                std_sms = message.text.format(c=level, n=name, r=roll)
                result = send_sms(std_sms, note, [s.contact], api_key, username)
                success += int(result['success'])

            attendance = AttendanceDate.objects.get(id=id)
            level = attendance.level_name
            student = Student.objects.filter(student_level=level)
            if student:
                self.context['student'] = Student.objects.filter(student_level=level)
                self.context['form'] = AttendanceForm
                self.context['att'] = AttendanceDate.objects.get(id=id)
                self.context['message'] = Message.objects.filter(institute=institutes[0])
                self.context['success'] = "{} message(s) send successfully.".format(success)
                return render(request, self.template_name, self.context)


class SelectAttendanceLevel(View):
    template_name = 'attendance/select_level.html'
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        else:
            context = {
                'level': Level.objects.filter(institute_name=institutes[0])

            }
            return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect('1234')
        else:
            level = request.POST['level']
            date = request.POST['date']

            attendance = AttendanceDate.objects.all()
            for a in attendance:
                dates = datetime.strptime(str(a.date), '%Y-%m-%d').strftime('%d-%m-%Y')
                if str(a.level_name.id) == level and dates == date:
                    return HttpResponseRedirect('/attendance/list/' + str(level) + '/' + str(date) + '/')
            else:
                context = {
                    'error': "Attendance Not Exist",
                    'level': Level.objects.filter(institute_name=institutes[0]),
                    'level_name': Level.objects.get(id=level),
                    'date': date
                }
                return render(request, self.template_name, context)


class AttendanceList(View):
    template_name = 'attendance/attendance_list.html'

    def get(self, request, id, date):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect('1234')
        else:
            level = Level.objects.get(id=id, institute_name=institutes[0])
            date = datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
            attendance_date = AttendanceDate.objects.get(date=date, level_name=level)
            attendance = AttendanceStudent.objects.filter(attendance_date=attendance_date, attendance=False)
            date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
            context = {
                'attendance': attendance,
                'date': date,
                'id': attendance_date,

            }

            return render(request, self.template_name, context)


class EditAttendance(View):
    template_name = 'attendance/edit.html'

    def get(self, request, id, date):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        else:
            att = AttendanceStudent.objects.filter(attendance_date__id=id)
            context = {
                'attendance': att,
                'message': Message.objects.filter(institute=institutes[0])
            }
            return render(request, self.template_name, context)

    def post(self, request, id, date):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        else:
            if 'save' in request.POST:
                get_students = request.POST.getlist('student')
                students = [int(s) for s in get_students]
                attendance_date = AttendanceDate.objects.get(id=id)
                level_students = Student.objects.filter(student_level=attendance_date.level_name)

                for student in level_students:
                    obj, created = AttendanceStudent.objects.get_or_create(attendance_date=attendance_date,
                                                                           student_name=student)
                    if student.id in students:
                        obj.attendance = False
                        obj.save()
                    else:
                        obj.attendance = True
                        obj.save()
                return HttpResponseRedirect('/attendance/')

            else:
                get_students = request.POST.getlist('student')
                students = [int(s) for s in get_students]
                attendance_date = AttendanceDate.objects.get(id=id)
                level_students = Student.objects.filter(student_level=attendance_date.level_name)

                for student in level_students:
                    obj, created = AttendanceStudent.objects.get_or_create(attendance_date=attendance_date,
                                                                           student_name=student)
                    if student.id in students:
                        obj.attendance = False
                        obj.save()
                    else:
                        obj.attendance = True
                        obj.save()
                ss = [int(s) for s in get_students]
                stds = Student.objects.filter(id__in=ss)
                contacts = [s.contact for s in stds]
                message = Message.objects.get(id=int(request.POST.get('msg_id', 0)))

                note = "To contacts " + ','.join(contacts)
                institute = Institute.objects.get(user=request.user)
                api_key = institute.sms_api_key
                username = institute.sms_username
                success = 0
                for s in stds:
                    level = s.student_level
                    name = s.full_name
                    roll = s.student_id
                    std_sms = message.text.format(c=level, n=name, r=roll)
                    result = send_sms(std_sms, note, [s.contact], api_key, username)
                    success += int(result['success'])
                attendance = AttendanceDate.objects.get(id=id)
                level = attendance.level_name
                student = Student.objects.filter(student_level=level)
                if student:
                    context = {
                        'student': Student.objects.filter(student_level=level),
                        'form': AttendanceForm,
                        'att': AttendanceDate.objects.get(id=id),
                        'message': Message.objects.filter(institute=institutes[0]),
                        'success': "{} message(s) send successfully.".format(success)
                    }
                    return render(request, self.template_name, context)


class TeacherAttendanceDateView(View):
    template_name = 'attendance/teacher_attendance_date.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        context = {
            'form': TeacherAttendaceForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        form = TeacherAttendaceForm(request.POST)
        institute = Institute.objects.get(user=request.user)

        attendance_date = TeacherAttendanceDate.objects.filter(institute = institutes[0].id)
        date = datetime.strptime(request.POST['date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        for att in attendance_date:
            if date == str(att.date):
                date = request.POST['date']
                context = {
                    'date': date
                }
                return render(request, self.template_name, context)

        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.institute = institute
            teacher.save()
            return HttpResponseRedirect('/attendance/teacher-attendance/' + str(teacher.id) + '/')


class TeacherAttendanceView(View):
    template_name = 'attendance/teacher_attendance.html'

    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        context = {
            'teacher': Teacher.objects.filter(institute=institutes[0].id),
            'message': Message.objects.filter(institute=institutes[0])
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        if 'save' in request.POST:
            get_teachers = request.POST.getlist('teacher')
            teachers = [int(s) for s in get_teachers]
            attendance_date = TeacherAttendanceDate.objects.get(id=id)
            institutes_teacher = Teacher.objects.filter(institute=institutes[0].id)
            for teacher in institutes_teacher:
                obj, created = AttendanceTeacher.objects.get_or_create(attendance_date=attendance_date,
                                                                       teacher=teacher)
                if teacher.id in teachers:
                    obj.attendance = False
                    obj.save()
                else:
                    obj.attendance = True
                    obj.save()
            return HttpResponseRedirect('/attendance/teacher')


        else:
            get_teachers = request.POST.getlist('teacher')
            teachers = [int(s) for s in get_teachers]
            attendance_date = TeacherAttendanceDate.objects.get(id=id)
            institutes_teacher = Teacher.objects.filter(institute=institutes[0].id)
            for teacher in institutes_teacher:
                obj, created = AttendanceTeacher.objects.get_or_create(attendance_date=attendance_date,
                                                                       teacher=teacher)
                if teacher.id in teachers:
                    obj.attendance = False
                    obj.save()
                else:
                    obj.attendance = True
                    obj.save()

            ss = [int(s) for s in get_teachers]
            inst_teacher = Teacher.objects.filter(id__in=ss)
            contacts = [s.contact for s in inst_teacher]
            message = Message.objects.get(id=int(request.POST.get('msg_id', 0)))
            note = "To contacts " + ','.join(contacts)
            institute = Institute.objects.get(user=request.user)
            api_key = institute.sms_api_key
            username = institute.sms_username
            success = 0
            for t in inst_teacher:
                level = ''
                name = t.full_name
                roll = t.teacher_id
                std_sms = message.text.format(c=level, n=name, r=roll)
                result = send_sms(std_sms, note, [t.contact], api_key, username)
                success += int(result['success'])

            teacher = Teacher.objects.filter(institute=institutes[0].id)
            if teacher:
                context = {
                    'teacher': Teacher.objects.filter(institute=institutes[0].id),
                    'form': TeacherAttendaceForm,
                    'att': TeacherAttendanceDate.objects.get(id=id),
                    'message': Message.objects.filter(institute=institutes[0]),
                    'success': "{} message(s) send successfully.".format(success)
                }
                return render(request, self.template_name, context)


class SelectAttendanceDateView(View):
    template_name = 'attendance/teacher_select_date.html'
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        else:

            return render(request, self.template_name)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect('1234')
        else:
            date = request.POST['date']
            attendance = TeacherAttendanceDate.objects.filter(institute=institutes[0].id)
            for a in attendance:
                dates = datetime.strptime(str(a.date), '%Y-%m-%d').strftime('%d-%m-%Y')
                if dates == date:
                    return HttpResponseRedirect('/attendance/teacher-absent-list/'+ str(date) + '/')
            else:
                context = {
                    'error': "Attendance Not Exist",
                    'date': date
                }
                return render(request, self.template_name, context)


class TeacherAttendanceListView(View):
    template_name = 'attendance/teacher_absent_list.html'

    def get(self, request, date):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect('1234')
        else:
            date = datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
            attendance_date = TeacherAttendanceDate.objects.get(date=date)
            attendance = AttendanceTeacher.objects.filter(attendance_date=attendance_date, attendance=False)

            date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
            context = {
                'attendance': attendance,
                'date': date,
                'attendance_date': attendance_date,

            }

            return render(request, self.template_name, context)


class TeacherAttendanceEditView(View):
    template_name = 'attendance/teacher_attendance_edit.html'

    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        att = AttendanceTeacher.objects.filter(attendance_date__id=id)
        context = {
            'attendance': att,
            'message': Message.objects.filter(institute=institutes[0])
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        if 'save' in request.POST:
            get_teachers = request.POST.getlist('teacher')
            teachers = [int(s) for s in get_teachers]
            attendance_date = TeacherAttendanceDate.objects.get(id=id)
            institutes_teacher = Teacher.objects.filter(institute=institutes[0].id)
            for teacher in institutes_teacher:
                obj, created = AttendanceTeacher.objects.get_or_create(attendance_date=attendance_date,
                                                                       teacher=teacher)
                if teacher.id in teachers:
                    obj.attendance = False
                    obj.save()
                else:
                    obj.attendance = True
                    obj.save()
            return HttpResponseRedirect('/attendance/select-date')


        else:
            get_teachers = request.POST.getlist('teacher')
            teachers = [int(s) for s in get_teachers]
            attendance_date = TeacherAttendanceDate.objects.get(id=id)
            institutes_teacher = Teacher.objects.filter(institute=institutes[0].id)
            for teacher in institutes_teacher:
                obj, created = AttendanceTeacher.objects.get_or_create(attendance_date=attendance_date,
                                                                       teacher=teacher)
                if teacher.id in teachers:
                    obj.attendance = False
                    obj.save()
                else:
                    obj.attendance = True
                    obj.save()

            ss = [int(s) for s in get_teachers]
            inst_teacher = Teacher.objects.filter(id__in=ss)
            contacts = [s.contact for s in inst_teacher]
            message = Message.objects.get(id=int(request.POST.get('msg_id', 0)))
            note = "To contacts " + ','.join(contacts)
            institute = Institute.objects.get(user=request.user)
            api_key = institute.sms_api_key
            username = institute.sms_username
            success = 0
            for t in inst_teacher:
                level = ''
                name = t.full_name
                roll = t.teacher_id
                std_sms = message.text.format(c=level, n=name, r=roll)
                result = send_sms(std_sms, note, [t.contact], api_key, username)
                success += int(result['success'])

            teacher = Teacher.objects.filter(institute=institutes[0].id)
            if teacher:
                context = {
                    'teacher': Teacher.objects.filter(institute=institutes[0].id),
                    'form': TeacherAttendaceForm,
                    'att': TeacherAttendanceDate.objects.get(id=id),
                    'message': Message.objects.filter(institute=institutes[0]),
                    'success': "{} message(s) send successfully.".format(success)
                }
                return render(request, self.template_name, context)
