from django import forms
from django.forms import Textarea
from .models import UserMessage


class UserMessageForm(forms.ModelForm):
    ''' Represents a form for users to write messages to the
    admin regarding an order.
    '''
    class Meta:
        ''' Fields in order form and type of field.
        '''
        model = UserMessage
        fields = (
            'user_message',
        )
        widgets = {
            'user_message': Textarea(attrs={'rows': 8}),
        }

    def __init__(self, *args, **kwargs):
        ''' Remove Label and add placeholder from user message form
        '''
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False
            if field == 'user_message':
                self.fields[field].widget.attrs[
                    'placeholder'] = 'Reply to this thread here...'
