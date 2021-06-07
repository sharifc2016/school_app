from django import forms
from teacher.models import Teacher


class TeacherForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'), input_formats=('%d-%m-%Y',))

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter date of birth'})

        self.fields['teacher_id'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Teacher ID'})

        self.fields['join_year'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter admission year'})

        self.fields['full_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter full name'})

        self.fields['father_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter father name'})

        self.fields['mother_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter mother name'})

        self.fields['address'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter address here'})

        self.fields['contact'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter contact number'})

        self.fields['image'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Select an image'})

        self.fields['extra'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter your opinion'})


    class Meta:
        # Meta class is used for additional information about the model that is used for create ModelForm
        model = Teacher
        fields = ['teacher_id', 'full_name', 'father_name', 'mother_name', 'join_year', 'dob',
                  'address', 'contact','image','extra']
