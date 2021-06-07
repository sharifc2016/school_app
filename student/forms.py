from django import forms
from student.models import Student


# Student add
class StudentAddForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'), input_formats=('%d-%m-%Y',))

    def __init__(self, institute, *args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)
        self.fields['dob'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter date of birth'})

        self.fields['student_id'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter student roll'})

        self.fields['student_level'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter student level or class', 'required' : True})

        self.fields['admission_year'].widget.attrs.update(
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
            {'class': 'form-control', 'placeholder': 'Enter contact number (11 digit)'})

        self.fields['image'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Select an image'})

        self.fields['extra'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter your opinion'})
        self.fields['student_level'].queryset = self.fields['student_level'].queryset.filter(
            institute_name__id=institute)

    class Meta:
        # Meta class is used for additional information about the model that is used for create ModelForm
        model = Student
        fields = ['student_id', 'student_level', 'full_name', 'father_name', 'mother_name', 'admission_year', 'dob',
                  'address', 'contact','image','extra']
