from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.views import View

from institute.models import Institute
from level.forms import LevelForm
from level.models import Level
from student.models import Student
from template_messages.models import Message
from template_messages.views import send_sms


class AddLevel(View):
    template_name = "level/add.html"
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        self.context['level'] = LevelForm

        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        form = LevelForm(request.POST)
        institute = Institute.objects.get(user=request.user)

        if form.is_valid():
            level = form.save(commit=False)
            level.institute_name = institute
            level.save()
            return HttpResponseRedirect('/level/list')

        return HttpResponseRedirect('/')


class LevelList(View):
    template_name = 'level/list.html'
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        self.context['level'] = Level.objects.filter(institute_name=institutes[0])
        self.context['message'] = Message.objects.filter(institute=institutes[0])

        return render(request, self.template_name, self.context)


class EditLevel(View):
    template_name = 'level/edit.html'
    context = {}

    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        user_name = request.user.username

        level = Level.objects.get(id=id)
        self.context['level'] = LevelForm(instance=level)
        return render(request, self.template_name, self.context)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        if 'save' in request.POST:
            level = Level.objects.get(id=id)
            form = LevelForm(request.POST, instance=level)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse('level-list'))
        return HttpResponseRedirect(reverse('/'))


class DeleteLevel(View):

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        user_name = request.user.username

        if request.method == 'POST':

            if 'delete' in request.POST:
                id = int(request.POST['student-id'])
                level = Level.objects.get(id=id)
                level.delete()

        return HttpResponseRedirect(reverse('level-list'))


class MigrationsLevelView(View):
    template_name = 'level/select_migrations_level.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        migrations_level = Level.objects.filter(institute_name=institutes[0].id)

        context = {
            'migrations_level': migrations_level
        }

        return render(request, self.template_name, context)

    def post(self, request):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        level = request.POST['level']

        return HttpResponseRedirect('/level/migrations/' + str(level) + '/')


class StudentMigrationView(View):
    template = 'level/students_migrations.html'

    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        level = Level.objects.get(id=id)
        migrations_to = Level.objects.filter(institute_name=institutes[0].id)
        students = Student.objects.filter(student_level__id=id)

        context = {
            'students': students,
            'level': level,
            'migrations_to': migrations_to
        }

        return render(request, self.template, context)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        migrate_from = Level.objects.get(id=id)
        students = request.POST.getlist('student')
        get_level = request.POST['level']
        level = Level.objects.get(id=get_level)

        if migrate_from == level:
            context = {
                'error': "You can not migrate to the same class"
            }
            return render(request, self.template, context)
        for id in students:
            student = Student.objects.get(id=id)
            student.student_level = level
            student.save()

        success = len(students)
        context = {
            'success': "{} students migrate from {} to {}".format(success, migrate_from, level),
        }

        return render(request, 'level/students_migrations.html', context)


class LevelSmsView(View):

    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        get_students = Student.objects.filter(student_level__id=id)
        level = Level.objects.filter(institute_name=institutes[0].id)
        total_student = len(get_students)
        context = {
            'level' : level,
            'total_student': total_student,
            'level_name': Level.objects.get(id=id),
            'message': Message.objects.filter(institute=institutes[0]),
        }

        template_name = 'level/all-student-sms.html'
        return render(request, template_name, context)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        get_students = Student.objects.filter(student_level__id=id)
        if len(get_students) == 0:
            level = Level.objects.filter(institute_name=institutes[0].id)
            template_name = 'level/all-student-sms.html'
            if level:
                context = {
                    'level': level,
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

        level = Level.objects.filter(institute_name = institutes[0].id)
        template_name = 'level/all-student-sms.html'
        if level:
            context = {
                'level': level,
                'message': Message.objects.filter(institute=institutes[0]),
                'success': "{} message send successfully.".format(success)
            }

            return render(request, template_name, context)
        else:
            return redirect('level-list')