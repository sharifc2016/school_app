from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View
from institute.models import Institute
from level.models import Level
from subject.forms import SubjectForm
from subject.models import Subject


class AddSubject(View):
    template_name = "subject/add.html"
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        self.context['subject'] = SubjectForm(institute= institutes[0].id)

        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        form = SubjectForm(institutes[0].id, request.POST)
        institute = Institute.objects.get(user=request.user)

        if form.is_valid():
            subject = form.save(commit=False)
            subject.level_name__institute_name = institute
            subject.save()
            return HttpResponseRedirect('/subject/list')


class SubjectList(View):
    template_name = 'subject/list.html'
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        self.context['subject'] = Subject.objects.filter(level_name__institute_name= institutes[0])

        return render(request, self.template_name, self.context)

class EditSubject(View):
    template_name = 'subject/edit.html'
    context = {}

    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        subject = Subject.objects.get(id = id)
        self.context['subject'] = SubjectForm(institutes[0].id,instance = subject)
        return render(request, self.template_name, self.context)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))
        if 'save' in request.POST:
            subject = Subject.objects.get(id=id)
            form = SubjectForm(institutes[0].id,request.POST, instance=subject)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse('subject-list'))
        return HttpResponseRedirect(reverse('/'))


class DeleteSubject(View):

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
                subject = Subject.objects.get(id=id)
                subject.delete()

        return HttpResponseRedirect(reverse('subject-list'))

