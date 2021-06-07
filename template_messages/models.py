from django.db import models
from institute.models import Institute


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


class Message(models.Model):
    institute = models.ForeignKey(Institute, verbose_name="Institute")
    text = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.institute.name

    def message_size(self):
        message_length = len(str(self.text))
        if not is_ascii(self.text):
            message_length *= 2.5
        return int(message_length)

    def per_sms_size(self):
        return int(self.message_size() / 150 + 1)

    def is_unicode(self):
        return not is_ascii(self.text)

    def sms_type(self):
        if self.is_unicode():
            return 'UNICODE'
        else:
            return 'TEXT'
