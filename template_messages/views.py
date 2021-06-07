from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse
from django.views import View
from institute.models import Institute
from template_messages.forms import MessageForm
from template_messages.models import Message
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import re



class AddMessage(View):
    template_name = "template_messages/message.html"
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))


        self.context['message'] = MessageForm

        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        form = MessageForm(request.POST)
        institute = Institute.objects.get(user=request.user)

        if form.is_valid():
            message = form.save(commit=False)
            message.institute = institute
            message.save()
            return HttpResponseRedirect('/sms/')


class MessageList(View):
    template_name =  "template_messages/list.html"
    context = {}

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        self.context['message'] = Message.objects.filter(institute = institutes[0])

        return render(request, self.template_name, self.context)


class EditMessage(View):
    template_name = 'template_messages/edit.html'
    context = {}

    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        message = Message.objects.get(id=id)
        self.context['message'] = MessageForm(instance = message)

        return render(request, self.template_name, self.context)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        institutes = Institute.objects.filter(user=request.user)
        if not institutes:
            return HttpResponseRedirect(reverse('login'))

        if 'save' in request.POST:
            message = Message.objects.get(id=id)
            form = MessageForm(request.POST, instance=message)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse('sms-list'))
        return HttpResponseRedirect(reverse('/'))


class DeleteMessage(View):
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
                message = Message.objects.get(id=id)
                message.delete()

        return HttpResponseRedirect(reverse('sms-list'))


def send_sms(message, message_type, receiver,api_key, username, mask='NOMASK'):
    recipient = []
    for receive in receiver:
        pattern = re.compile("^(?:\+?88)?01[15-9]\d{8}$")
        if pattern.match(receive):
            recipient += [ '880' + receive[len(receive) - 10:len(receive) + 1] ]


    url = 'http://45.33.76.177:8000/api-v2/?format=json'  # Set destination URL here
    post_fields = {'mask': mask, 'api_key': api_key, 'user_name': username,
                   'MsgType': message_type, 'receiver': '|'.join(recipient), 'message': message}  # Set POST fields here

    r = Request(url, urlencode(post_fields).encode())
    json_data = urlopen(r).read().decode()
    data = json.loads(json_data)
    success = 0
    for d in data:
        if d['success'] == 1:
            success += 1
    result = {'json': json_data, 'total_send': len(receiver), 'success': success}

    return result




