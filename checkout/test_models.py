from decimal import Decimal
from django.test import TestCase

from products.models import Product
from mc_vinyl import settings
from .models import Order
from .models import OrderLineItem


class TestCheckoutModels(TestCase):

    def setUp(self):
        Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1.3',
        )

        Order.objects.create(
            full_name='test name',
            email='test@email.com',
            phone_number='123456',
            country='IE',
            town_or_city='test city',
            street_address1='test address 1',
        )

    # Test Order String Method
    #
    def test_order_string_method(self):
        order = Order.objects.get(email='test@email.com')
        self.assertEqual(str(order), order.order_number)

    # Test OrderLineItem Model
    #
    def test_order_line_item_model_with_delivery(self):
        order = Order.objects.get(email='test@email.com')
        product = Product.objects.get(sku='Test SKU')
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=product,
            quantity=2,
        )
        self.assertEqual(
            order_line_item.lineitem_total, Decimal(
                order_line_item.product.price * order_line_item.quantity)
        )
        self.assertEqual(order.delivery_cost, settings.STANDARD_DELIVERY_COST)

    def test_order_line_item_model_free_delivery(self):
        order = Order.objects.get(email='test@email.com')
        product = Product.objects.get(sku='Test SKU')
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=product,
            quantity=200,
        )
        self.assertEqual(
            order_line_item.lineitem_total, Decimal(
                order_line_item.product.price * order_line_item.quantity)
        )
        self.assertEqual(order.delivery_cost, 0)

    def test_order_line_item_string_method(self):
        order = Order.objects.get(email='test@email.com')
        product = Product.objects.get(sku='Test SKU')
        order_line_item = OrderLineItem.objects.create(
            order=order,
            product=product,
            quantity=200,
        )
        self.assertEqual(
            str(order_line_item),
            f'SKU {order_line_item.product.sku} on order {order_line_item.order.order_number}'
        )
