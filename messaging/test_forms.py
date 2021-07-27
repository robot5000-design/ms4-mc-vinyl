from django.test import TestCase

from django.contrib.auth.models import User
from messaging.forms import UserMessageForm
from messaging.models import UserMessage


class TestMessagingForm(TestCase):

    # Test Messaging form
    #
    def test_messaging_form_message_required(self):
        form = UserMessageForm({
            'user_message': ''
            })
        self.assertFalse(form.is_valid())
        self.assertIn('user_message', form.errors.keys())
        self.assertEqual(form.errors['user_message'][0],
                         'This field is required.')




