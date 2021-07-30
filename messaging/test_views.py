from django.test import TestCase
from django.contrib.messages import get_messages

from django.contrib.auth.models import User
from messaging.models import UserMessage
from checkout.models import Order
from profiles.models import UserProfile


class TestMessagingViews(TestCase):

    def setUp(self):
        testuser = User.objects.create_user(
            username='testuser', password='testpassword')
        testuser_su = User.objects.create_superuser(
            username='testuser_su', password='testpassword')

        testuser.save()
        testuser_su.save()

        testuser_profile = UserProfile.objects.get(user=testuser)

        UserMessage.objects.create(
            ref_number='123',
            user_message='test message'
        )

        Order.objects.create(
            order_number='123',
            full_name='test name',
            email='test@email.com',
            phone_number='test phone',
            country='US',
            postcode='test postcode',
            town_or_city='test city',
            street_address1='test address 1',
            county='test country',
            original_cart={},
            user_profile=testuser_profile
        )

    # Test Messaging View
    #
    def test_get_messaging_page(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.get('/messaging/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'messaging/messaging.html')

    def test_login_required_for_get_messaging_page(self):
        response = self.client.get('/messaging/')
        self.assertRedirects(response, '/accounts/login/?next=/messaging/')

    def test_superuser_required_for_messaging_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/messaging/')
        self.assertRedirects(response, '/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Sorry, only store owners can do that.')

    # Test Message Thread View
    #
    def test_get_message_thread_page(self):
        self.client.login(username='testuser_su', password='testpassword')
        message_thread = UserMessage.objects.filter(ref_number='123')
        response = self.client.get(
            f'/messaging/message_thread/{message_thread[0].ref_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'messaging/message_thread.html')

    def test_message_thread_does_not_exist(self):
        self.client.login(username='testuser_su', password='testpassword')
        ref_number = 321
        response = self.client.get(
            f'/messaging/message_thread/{ref_number}/')
        self.assertRedirects(response, '/messaging/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'That does not exist!')

    def test_superuser_required_get_message_thread_page(self):
        self.client.login(username='testuser', password='testpassword')
        message_thread = UserMessage.objects.filter(ref_number='123')
        response = self.client.get(
            f'/messaging/message_thread/{message_thread[0].ref_number}/')
        self.assertRedirects(response, '/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Sorry, only store owners can do that.')

    def test_login_required_get_message_thread_page(self):
        message_thread = UserMessage.objects.filter(ref_number='123')
        response = self.client.get(
            f'/messaging/message_thread/{message_thread[0].ref_number}/')
        self.assertRedirects(
            response, '/accounts/login/?next=/messaging/message_thread/123/')

    # Test Add Admin Reply View
    #
    def test_add_admin_reply_successful(self):
        self.client.login(username='testuser_su', password='testpassword')
        user = User.objects.get(username='testuser')
        message_thread = UserMessage.objects.filter(ref_number='123')
        response = self.client.post(
            f'/messaging/admin_reply/{message_thread[0].ref_number}/', {
                'ref_number': message_thread[0].ref_number,
                'user': user,
                'user_message': 'test admin message',
            })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully added a message!')
        self.assertRedirects(
            response, f'/messaging/message_thread/{message_thread[0].ref_number}/'
        )

    def test_superuser_required_add_admin_reply(self):
        self.client.login(username='testuser', password='testpassword')
        user = User.objects.get(username='testuser')
        message_thread = UserMessage.objects.filter(ref_number='123')
        response = self.client.post(
            f'/messaging/admin_reply/{message_thread[0].ref_number}/', {
                'ref_number': message_thread[0].ref_number,
                'user': user,
                'user_message': 'test admin message',
            })
        self.assertRedirects(response, '/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Sorry, only store owners can do that.')

    def test_add_admin_reply_invalid_form(self):
        self.client.login(username='testuser_su', password='testpassword')
        user = User.objects.get(username='testuser')
        message_thread = UserMessage.objects.filter(ref_number='123')
        response = self.client.post(
            f'/messaging/admin_reply/{message_thread[0].ref_number}/', {
                'ref_number': message_thread[0].ref_number,
                'user': user,
                'user_message': '',
            })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Failed to add message. Please ensure the form is valid.'
        )
        self.assertRedirects(
            response, f'/messaging/message_thread/{message_thread[0].ref_number}/'
        )

    def test_add_admin_reply_post_method_required(self):
        self.client.login(username='testuser_su', password='testpassword')
        user = User.objects.get(username='testuser')
        message_thread = UserMessage.objects.filter(ref_number='123')
        response = self.client.get(
            f'/messaging/admin_reply/{message_thread[0].ref_number}/', {
                'ref_number': message_thread[0].ref_number,
                'user': user,
                'user_message': 'test admin message',
            })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid Method.')
        self.assertRedirects(
            response, f'/messaging/message_thread/{message_thread[0].ref_number}/'
        )

    # Test Delete Thread View
    #
    def test_delete_thread_successful(self):
        self.client.login(username='testuser_su', password='testpassword')
        message_thread = UserMessage.objects.filter(ref_number='123')
        response = self.client.post(
            f'/messaging/delete_thread/{message_thread[0].ref_number}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Message Thread Deleted.')
        self.assertRedirects(response, '/messaging/')
        message_thread = UserMessage.objects.filter(ref_number='123')
        self.assertEqual(len(message_thread), 0)

    def test_login_required_delete_thread(self):
        message_thread = UserMessage.objects.filter(ref_number='123')
        response = self.client.post(
            f'/messaging/delete_thread/{message_thread[0].ref_number}/')
        self.assertRedirects(
            response,
            '/accounts/login/?next=/messaging/delete_thread/123/'
            )
        UserMessage.objects.get(ref_number='123')

    def test_superuser_required_delete_thread(self):
        self.client.login(username='testuser', password='testpassword')
        message_thread = UserMessage.objects.filter(ref_number='123')
        response = self.client.post(
            f'/messaging/delete_thread/{message_thread[0].ref_number}/')
        self.assertRedirects(response, '/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Sorry, only store owners can do that.')
        UserMessage.objects.get(ref_number='123')

    def test_post_method_required_delete_thread(self):
        self.client.login(username='testuser_su', password='testpassword')
        message_thread = UserMessage.objects.filter(ref_number='123')
        response = self.client.get(
            f'/messaging/delete_thread/{message_thread[0].ref_number}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid Method.')
        self.assertRedirects(response, '/messaging/')
        UserMessage.objects.get(ref_number='123')

    # Test Change Thread Status View
    #
    def test_change_thread_status_to_closed(self):
        self.client.login(username='testuser_su', password='testpassword')
        message_thread = UserMessage.objects.filter(ref_number='123')
        ref_number = message_thread[0].ref_number
        self.assertEqual(message_thread[0].closed, False)
        response = self.client.post(
            f'/messaging/change_thread_status/{ref_number}/')
        self.assertRedirects(
            response, f'/messaging/message_thread/{ref_number}/'
        )
        self.assertEqual(message_thread[0].closed, True)

    def test_change_thread_status_to_open(self):
        self.client.login(username='testuser_su', password='testpassword')
        message_thread = UserMessage.objects.filter(ref_number='123')
        ref_number = message_thread[0].ref_number
        last_message = message_thread[0]
        last_message.closed = True
        last_message.save()
        self.assertEqual(last_message.closed, True)
        response = self.client.post(
            f'/messaging/change_thread_status/{ref_number}/')
        self.assertRedirects(
            response, f'/messaging/message_thread/{ref_number}/'
        )
        self.assertEqual(message_thread[0].closed, False)

    def test_change_thread_status_index_error(self):
        self.client.login(username='testuser_su', password='testpassword')
        ref_number = 321
        response = self.client.post(
            f'/messaging/change_thread_status/{ref_number}/')
        self.assertRedirects(response, '/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'list index out of range')

    def test_login_required_change_thread_status(self):
        message_thread = UserMessage.objects.filter(ref_number='123')
        ref_number = message_thread[0].ref_number
        self.assertEqual(message_thread[0].closed, False)
        response = self.client.post(
            f'/messaging/change_thread_status/{ref_number}/')
        self.assertRedirects(
            response, f'/accounts/login/?next=/messaging/change_thread_status/{ref_number}/'
        )
        self.assertEqual(message_thread[0].closed, False)

    def test_superuser_required_change_thread_status(self):
        self.client.login(username='testuser', password='testpassword')
        message_thread = UserMessage.objects.filter(ref_number='123')
        ref_number = message_thread[0].ref_number
        self.assertEqual(message_thread[0].closed, False)
        response = self.client.post(
            f'/messaging/change_thread_status/{ref_number}/')
        self.assertRedirects(response, '/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Sorry, only store owners can do that.')
        self.assertEqual(message_thread[0].closed, False)

    def test_post_method_required_change_thread_status(self):
        self.client.login(username='testuser_su', password='testpassword')
        message_thread = UserMessage.objects.filter(ref_number='123')
        ref_number = message_thread[0].ref_number
        self.assertEqual(message_thread[0].closed, False)
        response = self.client.get(
            f'/messaging/change_thread_status/{ref_number}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid Method.')
        self.assertRedirects(
            response, f'/messaging/message_thread/{ref_number}/'
        )
        self.assertEqual(message_thread[0].closed, False)
