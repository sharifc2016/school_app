from django.forms import ModelForm
from django import forms
from attendance.models import *


class AttendanceDateForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'), input_formats=('%d-%m-%Y',))

    def __init__(self, institute, *args, **kwargs):
        super(AttendanceDateForm, self).__init__(*args, **kwargs)
        self.fields['level_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Level', 'required': True})
        self.fields['date'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Date', 'required': True})
        self.fields['level_name'].queryset = self.fields['level_name'].queryset.filter(institute_name__id=institute)

    class Meta:
        model = AttendanceDate
        fields = ['level_name', 'date']


class AttendanceForm(ModelForm):
    class Meta:
        model = AttendanceStudent
        fields = ['attendance']


class TeacherAttendaceForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'), input_formats=('%d-%m-%Y',))
    def __init__(self, *args, **kwargs):
        super(TeacherAttendaceForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Date', 'required': True})

    class Meta:
        model = TeacherAttendanceDate
        fields = ['date']
