from django.test import TestCase

from .forms import OrderForm
from .models import Order


class TestCheckoutForms(TestCase):

    # Test Order form
    #
    def test_add_order_form_successful_with_required_fields(self):
        form = OrderForm({
            'full_name': 'test name',
            'email': 'test@email.com',
            'phone_number': '123456',
            'country': 'IE',
            'town_or_city': 'test city',
            'street_address1': 'test address 1',
            })
        self.assertTrue(form.is_valid())
        form.save()
        Order.objects.get(email='test@email.com')
