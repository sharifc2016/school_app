from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from institute.models import Institute
from teacher.forms import TeacherForm
from teacher.models import Teacher
from template_messages.models import Message
from template_messages.views import send_sms


class TeacherAdd(View):
    template_name = 'teacher/add.html'

    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('/'))

        form = TeacherForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('/'))

        form = TeacherForm(request.POST, request.FILES)
        institute = Institute.objects.get(user=request.user)

        if form.is_valid():
            teacher = form.save(commit=False)
            # Create user
            teacher_id = form['teacher_id'].value()
            short_name = institute.short_name
            username = short_name + "t" + str(teacher_id)
            password = "teacher@2017"
            users = User.objects.all()
            for user in users:
                if user.username == str(institute.short_name) + "t" + str(teacher_id):
                    error_message = 'This teacher_id is already exist!'
                    return render(request, 'teacher/add.html', {'form': form, 'error_message': error_message})

            user = User.objects.create_user(username=username, password=password)
            teacher.user = user
            user.save()
            teacher.institute = institute
            teacher.save()
            return HttpResponseRedirect(reverse('teacher-list'))

        return render(request, 'teacher/list.html', {'form': form})


class TeacherList(View):
    template_name = 'teacher/list.html'

    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('/'))

        teacher = Teacher.objects.filter(institute=institutes[0].id)

        context = {
            'teacher': teacher,
        }
        return render(request, self.template_name, context)


class TeacherEdit(View):
    template_name = 'teacher/edit.html'

    def get(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('/'))
        teacher = Teacher.objects.get(pk=id)

        context = {
            'form': TeacherForm(instance=teacher)
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('/'))
        institute = Institute.objects.get(user=request.user)
        teacher = Teacher.objects.get(id=id)
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        teacher_id = form['teacher_id'].value()
        if form.is_valid():
            form = form.save(commit=False)
            user = teacher.user
            short_name = institute.short_name
            user.username = short_name + "t" + str(teacher_id)
            user.save()
            form.save()
            return HttpResponseRedirect('/teacher/list/')
        return render(request, 'teacher/edit.html', {'form': form})


class TeacherDetails(View):
    template_name = 'teacher/detail.html'

    def get(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('/'))
        context = {
            'teacher': Teacher.objects.get(id=id)
        }

        return render(request, self.template_name, context)

    def post(self, request, id):

        teacher = Teacher.objects.get(pk=id)
        template_name = 'student/detail.html'

        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        username = 'dpsc' + str(teacher.teacher_id)

        if len(pass1) < 6:
            context = {
                'teacher': teacher,
                'password': "Password must be at least 6 characture"
            }
        elif pass1 == pass2:
            user = User.objects.get(username=username)
            user.set_password(pass2)
            user.save()
            context = {
                'teacher': teacher,
                'password1': "Password Changed Succesfully"
            }
        else:
            context = {
                'teacher': teacher,
                'password': "Password not matched"
            }
        return render(request, template_name, context)


class TeacherDelete(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('/'))
        if 'delete' in request.POST:
            id = int(request.POST['teacher-id'])
            teacher = Teacher.objects.get(id=id)
            user = teacher.user
            user.delete()
        return HttpResponseRedirect(reverse('teacher-list'))


class TeacherSendSmsView(View):
    def get(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('/'))

        template_name = 'teacher/teacher_sms.html'
        context = {
            'teacher': Teacher.objects.get(id=id)
        }
        return render(request, template_name, context)

    def post(self, request, id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('/'))

        teacher = Teacher.objects.get(id=id)
        contact_number = teacher.contact
        message = request.POST['msg']
        note = "To contacts " + ','.join(contact_number)
        institute = Institute.objects.get(user=request.user)
        api_key = institute.sms_api_key
        username = institute.sms_username
        success = 0
        name = teacher.full_name
        roll = teacher.teacher_id
        std_sms = message.format(n=name, r=roll)
        result = send_sms(std_sms, note, [teacher.contact], api_key, username)
        success += int(result['success'])

        template_name = 'teacher/list.html'
        teacher = Teacher.objects.filter(institute=institutes[0])
        context = {
            'teacher': teacher,
            'success': "{} message(s) send successfully.".format(success),
        }
        return render(request, template_name, context)


class AllTeacherSmsView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('teacher-list'))

        template_name = 'teacher/all-teacher-sms.html'
        get_teachers = Teacher.objects.filter(institute=institutes[0].id)
        total_teacher = len(get_teachers)
        context = {
            'total_teacher': total_teacher,
            'message': Message.objects.filter(institute=institutes[0].id)
        }
        return render(request, template_name, context)

    def post(self, request):
        template_name = 'teacher/all-teacher-sms.html'
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        get_teachers = Teacher.objects.filter(institute=institutes[0])
        if len(get_teachers) == 0:
            template_name = 'student/all-student-sms.html'
            context = {
                'total_student': len(get_teachers),
                'error_message': "There is no student to this level, Please add student first."
            }
            return render(request, template_name, context)
        student = []
        for s in get_teachers:
            student += [s.id]
        success = 0
        for i in range(0, len(student), 100):
            stds = student[i:i + 100]
            ss = [int(s) for s in stds]
            teachers = Teacher.objects.filter(id__in=ss)
            contacts = [s.contact for s in teachers]
            message = request.POST['msg']
            note = "To contacts " + ','.join(contacts)
            institute = Institute.objects.get(user=request.user)
            api_key = institute.sms_api_key
            username = institute.sms_username

            for s in teachers:
                level = " "
                name = s.full_name
                roll = s.teacher_id
                std_sms = message.format(c=level, n=name, r=roll)
                result = send_sms(std_sms, note, [s.contact], api_key, username)
                success += int(result['success'])
        #
        teacher = Teacher.objects.filter(institute=institutes[0])
        if teacher:
            context = {
                'total_student': len(teacher),
                'success': "{} message send successfully.".format(success)
            }
            return render(request, template_name, context)
        else:
            return redirect('teacher-list')

#
# class TeacherPrint(View):
#     template_name = 'teacher/print.html'
#
#     def get(self, request, id):
#         if not request.user.is_authenticated():
#             return HttpResponseRedirect(reverse('login'))
#         institutes = Institute.objects.filter(user=request.user)
#         if not institutes:
#             return HttpResponseRedirect(reverse('/'))
#         context = {
#             'teacher': Teacher.objects.get(id=id)
#         }
#
#         return render(request, self.template_name, context)
