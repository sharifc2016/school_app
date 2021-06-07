from django import forms
from django.forms import ModelForm

from institute.models import Institute
from task.models import TaskInfo
from level.models import Level


class TaskInfoForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'), input_formats=('%d-%m-%Y',))

    def __init__(self, user, *args, **kwargs):
        super(TaskInfoForm, self).__init__(*args, **kwargs)
        self.fields['level'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter level here'})

        self.fields['date'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter date here'})

        self.fields['image_url'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter image url here'})
        self.fields['level'].queryset = Level.objects.filter(institute_name__user=user)

    class Meta:
        model = TaskInfo
        fields = ['level', 'date', 'image_url']
