from django.contrib.auth.models import User
from django.forms import ModelForm
from subject.models import Subject


class SubjectForm(ModelForm):
    def __init__(self,institute, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Subject', 'required': True})
        self.fields['level_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Level', 'required': True})
        self.fields['level_name'].queryset = self.fields['level_name'].queryset.filter(institute_name__id=institute)

    class Meta():
        model = Subject
        fields = ['name','level_name']
