from django.forms import ModelForm
from .models import Message


class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Message', 'required': True})

    class Meta():
        model = Message
        fields = ['text']
