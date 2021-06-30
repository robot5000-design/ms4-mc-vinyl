from django import forms
from django.forms import Textarea
from .models import UserMessage


class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = (
            'user_message',
        )
        widgets = {
            'user_message': Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)
