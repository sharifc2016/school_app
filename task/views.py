import datetime
import webbrowser
from urllib.request import urlopen

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View

from institute.models import Institute
from level.models import Level
from subject.models import Subject
from task.models import TaskInfo
from .models import Task
from .forms import TaskInfoForm


class AddTaskInfo(View):
    template_name = 'task/add-1.html'
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        self.context['now'] = datetime.datetime.now().strftime("%d-%m-%Y")
        self.context['class'] = Level.objects.filter(institute_name=institutes[0])
        self.context['form'] = TaskInfoForm(request.user)
        self.context['task_level'] = None
        self.context['success'] = None
        self.context['url'] = None
        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        level = Level.objects.get(id=int(request.POST.get('level')))
        date = request.POST.get('date')
        date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')

        info = TaskInfo.objects.filter(date=date, level=level)

        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
        image_url = request.POST.get('image_url')
        if info:
            self.context['task_level'] = level.id
            self.context['date'] = date
            self.context['success'] = None
            self.context['url'] = None
            return render(request, self.template_name, self.context)
        else:
            form = TaskInfoForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                self.context['now'] = datetime.datetime.now().strftime("%d-%m-%Y")
                self.context['class'] = Level.objects.filter(institute_name=institutes[0])
                self.context['form'] = TaskInfoForm(request.user)
                self.context['success'] = 'Task add successfully'
                self.context['url'] = None
                self.context['task_level'] = None
                return HttpResponseRedirect(reverse('task_list'))
            else:
                self.context['class'] = Level.objects.filter(institute_name=institutes[0])
                self.context['form'] = TaskInfoForm(request.user)
                self.context['url'] = """ Please Enter A Valid URL """
                self.context['success'] = None
                self.context['task_level'] = None
                return render(request, self.template_name, self.context)


class SelectLevel(View):
    template_name = 'task/list-1.html'
    template_name_2 = 'task/task_view.html'
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        self.context['task'] = Level.objects.filter(institute_name=institutes[0])
        self.context['now'] = datetime.datetime.now().strftime("%d-%m-%Y")
        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        level = Level.objects.get(id=request.POST['level'])
        date = request.POST['date']
        date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
        t = TaskInfo.objects.all()
        for i in t:
            if str(i.date) == date and i.level == level:
                task = TaskInfo.objects.get(date=date, level=level)
                context = {
                    'image_url': task.image_url
                }
                return render(request, self.template_name_2, context)
        else:
            context = {
                'task': Level.objects.filter(institute_name=institutes[0]),
                'now': datetime.datetime.now().strftime("%d-%m-%Y"),
                'error': "No Record Found"
            }
            return render(request, self.template_name, context)


class TaskList(View):
    template_name = 'task/list-task.html'
    template_name_2 = 'task/task_view.html'
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        task = TaskInfo.objects.filter(level__institute_name=institutes[0])
        self.context['task'] = task
        return render(request, self.template_name, self.context)


class ViewTask(View):
    template_name = 'task/task_view.html'
    context = {}

    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        print(id)
        task = TaskInfo.objects.get(id=id)
        print(task)
        context = {
            'image_url': task.image_url
        }
        return render(request, self.template_name, context)


class Error(View):
    template_name = 'task/error.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        return render(request, self.template_name)


class EditTask(View):
    template_name = 'task/edit-task.html'
    context = {}

    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        task = TaskInfo.objects.get(id=id)
        self.context['now'] = datetime.datetime.now().strftime("%d-%m-%Y")
        self.context['class'] = Level.objects.filter(institute_name=institutes[0])
        self.context['form'] = TaskInfoForm(request.user, instance=task)
        self.context['task_level'] = None
        self.context['success'] = None
        self.context['url'] = None
        return render(request, self.template_name, self.context)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        task = TaskInfo.objects.get(id=id)
        level = Level.objects.get(id=int(request.POST.get('level')))
        date = request.POST.get('date')
        request_date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
        info = TaskInfo.objects.filter(date=request_date, level=level)
        all_task_date = TaskInfo.objects.filter(level__institute_name=institutes[0])
        date = datetime.datetime.strptime(request_date, '%Y-%m-%d').strftime('%d-%m-%Y')
        flag = True
        for t in all_task_date:
            if str(task.date) == str(request_date) and str(task.level.id) == str(level.id):
                flag = False
            elif str(request_date) == str(t.date) and str(t.level.id) == str(level.id):
                flag = True
                break
            else:
                flag = False

        if flag == True:
            self.context['task_level'] = level.id
            self.context['date'] = date
            self.context['success'] = None
            self.context['url'] = None
            return render(request, self.template_name, self.context)
        elif flag == False:
            form = TaskInfoForm(request.user, request.POST, instance=task)
            if form.is_valid():
                form.save()
                self.context['now'] = datetime.datetime.now().strftime("%d-%m-%Y")
                self.context['class'] = Level.objects.filter(institute_name=institutes[0])
                self.context['form'] = TaskInfoForm
                self.context['success'] = 'Task Update successfully'
                self.context['url'] = None
                self.context['task_level'] = None
                return HttpResponseRedirect(reverse('task_list'))
            else:
                task = TaskInfo.objects.get(id=id)
                self.context['now'] = datetime.datetime.now().strftime("%d-%m-%Y")
                self.context['class'] = Level.objects.filter(institute_name=institutes[0])
                self.context['form'] = TaskInfoForm(request.user, instance=task)
                self.context['url'] = """ Please Enter A Valid URL """
                self.context['success'] = None
                self.context['task_level'] = None
                return render(request, self.template_name, self.context)


class DeleteTask(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        id = request.POST.get('task_id')
        t = TaskInfo.objects.get(id=id)
        t.delete()
        return HttpResponseRedirect('/task/task-list/')


def search_date(date_list, date):
    for i in date_list:
        if i.date == date:
            return i.date
