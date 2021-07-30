from django.test import TestCase
from django.contrib.messages import get_messages

from django.contrib.auth.models import User
from checkout.models import Order
from profiles.models import UserProfile


class TestCheckoutViews(TestCase):

    def setUp(self):
        testuser = User.objects.create_user(
            username='testuser', password='testpassword')
        testuser_su = User.objects.create_superuser(
            username='testuser_su', password='testpassword')

        testuser.save()
        testuser_su.save()

        testuser_profile = UserProfile.objects.get(user=testuser)

        Order.objects.create(
            full_name='test name',
            email='test@email.com',
            phone_number='123456',
            country='IE',
            town_or_city='test city',
            street_address1='test address 1',
            user_profile=testuser_profile
        )

    # Test Checkout View
    #
    def test_checkout_view_redirect_empty_cart(self):
        response = self.client.get('/checkout/')
        self.assertRedirects(response, '/products/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "There's nothing in your cart at the moment")

    # Test All Orders View
    #
    def test_view_all_orders_page(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.get('/checkout/all_orders/')
        self.assertTemplateUsed(response, 'checkout/all_orders.html')

    def test_login_required_view_all_orders_page(self):
        response = self.client.get('/checkout/all_orders/')
        self.assertRedirects(
            response, '/accounts/login/?next=/checkout/all_orders/')

    def test_superuser_required_view_all_orders_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/checkout/all_orders/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Sorry, only store owners can do that.')
        self.assertRedirects(response, '/')

    def test_search_all_orders_page_blank_search(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.get('/checkout/all_orders/', {
            'search_users': ''
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "You didn't enter any search criteria!")
        self.assertRedirects(response, '/checkout/all_orders/')

    def test_search_all_orders_page_no_account(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.get('/checkout/all_orders/', {
            'search_users': 'no account'
        })
        self.assertTemplateUsed(response, 'checkout/all_orders.html')

    def test_search_all_orders_page_valid_search(self):
        self.client.login(username='testuser_su', password='testpassword')
        order = Order.objects.get(email='test@email.com')
        response = self.client.get('/checkout/all_orders/', {
            'search_users': 'testuser'
        })
        self.assertTemplateUsed(response, 'checkout/all_orders.html')

    # Test Order Detail View
    #
    def test_view_order_detail_page(self):
        self.client.login(username='testuser_su', password='testpassword')
        order = Order.objects.get(email='test@email.com')
        response = self.client.get(
            f'/checkout/order_detail/{order.order_number}/')
        self.assertTemplateUsed(response, 'checkout/order_detail.html')

    def test_login_required_view_order_detail_page(self):
        order = Order.objects.get(email='test@email.com')
        response = self.client.get(
            f'/checkout/order_detail/{order.order_number}/')
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/checkout/order_detail/{order.order_number}/'
            )

    def test_superuser_required_view_order_detail_page(self):
        self.client.login(username='testuser', password='testpassword')
        order = Order.objects.get(email='test@email.com')
        response = self.client.get(
            f'/checkout/order_detail/{order.order_number}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Sorry, only store owners can do that.')
        self.assertRedirects(response, '/')
