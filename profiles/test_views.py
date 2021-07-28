from django.test import TestCase
from django.contrib.messages import get_messages

from django.contrib.auth.models import User
from products.models import Product
from messaging.models import UserMessage
from checkout.models import Order
from profiles.models import UserProfile


class TestProfileViews(TestCase):

    def setUp(self):
        testuser = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@email.com')
        testuser.save()

        testuser_2 = User.objects.create_user(
            username='testuser2',
            password='testpassword',
            email='test@email.com')
        testuser_2.save()

        testuser_profile = UserProfile.objects.get(user=testuser)

        Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )

        Order.objects.create(
            order_number='123',
            user_profile=testuser_profile,
            full_name='test name',
            email='test@email.com',
            phone_number='test phone',
            country='US',
            postcode='test postcode',
            town_or_city='test city',
            street_address1='test address 1',
            county='test country',
            original_cart={},
        )

    # Test Profile View
    #
    def test_get_profile_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_post_request_get_profile_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/profile/')
        self.assertRedirects(response, '/profile/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Profile updated successfully')

    # Test Order History View
    #
    def test_get_order_detail_page(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        order = Order.objects.get(email=test_user.email)
        response = self.client.get(
            f'/profile/order_history/{order.order_number}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/past_order.html')

    def test_get_order_detail_user_does_not_match_order(self):
        self.client.login(username='testuser2', password='testpassword')
        test_user = User.objects.get(username='testuser')
        order = Order.objects.get(email=test_user.email)
        response = self.client.get(
            f'/profile/order_history/{order.order_number}/')
        self.assertRedirects(response, '/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Order does not match user!')

    def test_get_order_detail_user_does_not_match_anonymous_order(self):
        self.client.login(username='testuser2', password='testpassword')
        order = Order.objects.create(
            order_number='888',
            full_name='test name',
            email='test@email.com',
            phone_number='test phone',
            country='US',
            postcode='test postcode',
            town_or_city='test city',
            street_address1='test address 1',
            county='test country',
            original_cart={},
        )
        response = self.client.get(
            f'/profile/order_history/{order.order_number}/')
        self.assertRedirects(response, '/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Order does not match user!')

    # Test Add User Message View
    #
    def test_add_user_message_successful(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        order = Order.objects.get(user_profile__user=test_user)
        response = self.client.post(
            f'/profile/add_user_message/{order.order_number}/', {
                'user_message': 'test message'
            })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully added a message!')
        UserMessage.objects.get(user=test_user)

    def test_post_method_required_add_user_message(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        order = Order.objects.get(user_profile__user=test_user)
        response = self.client.get(
            f'/profile/add_user_message/{order.order_number}/', {
                'user_message': 'test message'
            })
        self.assertRedirects(
            response, f'/profile/order_history/{order.order_number}/')
        message = UserMessage.objects.filter(ref_number=order.order_number)
        self.assertEqual(len(message), 0)
