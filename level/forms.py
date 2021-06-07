from django.forms import ModelForm
from level.models import Level


class LevelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Level', 'required': True})
        self.fields['room'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Room'})

    class Meta():
        model = Level
        fields = ['name', 'room']
