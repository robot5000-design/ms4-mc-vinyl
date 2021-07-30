from django.test import TestCase
from django.contrib.messages import get_messages

from django.contrib.auth.models import User
from products.models import Product


class TestCartViews(TestCase):

    def setUp(self):
        Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )

    # Test Cart View
    #
    def test_get_cart_page(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
    
    # Test Add to Cart View
    #
    def test_add_to_cart_empty_cart(self):
        product = Product.objects.get(sku='Test SKU')
        response = self.client.get(f'/cart/add/{product.id}/')
        self.assertRedirects(response, '/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart[str(product.id)], 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Added item to your cart.')

    def test_add_to_cart_non_empty_cart(self):
        product = Product.objects.get(sku='Test SKU')
        response = self.client.get(f'/cart/add/{product.id}/')
        self.assertRedirects(response, '/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart[str(product.id)], 1)
        response = self.client.get(f'/cart/add/{product.id}/')
        cart = self.client.session['cart']
        self.assertEqual(cart[str(product.id)], 2)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            f'Updated item quantity to {cart[str(product.id)]}')

    def test_add_to_cart_quantity_5(self):
        product = Product.objects.get(sku='Test SKU')
        response = self.client.post(f'/cart/add/{product.id}/', {
            'quantity': 5
        })
        self.assertRedirects(response, '/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart[str(product.id)], 5)

    def test_add_to_cart_redirect_to_product_page(self):
        product = Product.objects.get(sku='Test SKU')
        response = self.client.post(f'/cart/add/{product.id}/', {
            'quantity': 5,
            'redirect_url': f'/products/{product.id}/'
        })
        self.assertRedirects(response, f'/products/{product.id}/')
        cart = self.client.session['cart']
        self.assertEqual(cart[str(product.id)], 5)

    # Test Adjust to Cart View
    #
    def test_adjust_cart_quantity_to_5(self):
        product = Product.objects.get(sku='Test SKU')
        response = self.client.post(f'/cart/adjust/{product.id}/', {
            'quantity': 5
        })
        self.assertRedirects(response, '/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart[str(product.id)], 5)
        messages = list(get_messages(response.wsgi_request))     
        self.assertEqual(
            str(messages[0]),
            f'Updated item quantity to {cart[str(product.id)]}')

    def test_adjust_cart_quantity_to_0(self):
        product = Product.objects.get(sku='Test SKU')
        response = self.client.post(f'/cart/add/{product.id}/', {
            'quantity': 5
        })
        self.assertRedirects(response, '/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart[str(product.id)], 5)
        response = self.client.post(f'/cart/adjust/{product.id}/', {
            'quantity': 0
        })
        self.assertRedirects(response, '/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart, {})
        messages = list(get_messages(response.wsgi_request))     
        self.assertEqual(str(messages[0]), 'Removed item from your cart.')

    def test_post_required_adjust_cart(self):
        product = Product.objects.get(sku='Test SKU')
        response = self.client.post(f'/cart/add/{product.id}/')
        cart = self.client.session['cart']
        self.assertEqual(cart[str(product.id)], 1)
        response = self.client.get(f'/cart/adjust/{product.id}/', {
            'quantity': 5
        })
        self.assertRedirects(response, '/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart[str(product.id)], 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'Invalid Method!')

    def test_adjust_cart_quantity_key_error(self):
        product = Product.objects.get(sku='Test SKU')
        response = self.client.post(f'/cart/adjust/{product.id}/', {
            'quantity': 0
        })
        self.assertRedirects(response, '/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart, {})
        messages = list(get_messages(response.wsgi_request))     
        self.assertEqual(
            str(messages[0]), f"Error removing item: '{product.id}'")

    def test_remove_from_cart(self):
        product = Product.objects.get(sku='Test SKU')
        response = self.client.post(f'/cart/add/{product.id}/')
        cart = self.client.session['cart']
        self.assertEqual(cart[str(product.id)], 1)
        response = self.client.post(f'/cart/remove/{product.id}/')
        self.assertRedirects(response, '/cart/')
        cart = self.client.session['cart']
        self.assertEqual(cart, {})
        messages = list(get_messages(response.wsgi_request))     
        self.assertEqual(str(messages[1]), 'Removed item from your cart')

    def test_remove_from_cart_key_error(self):
        product = Product.objects.get(sku='Test SKU')
        response = self.client.post(f'/cart/remove/{product.id}/')
        self.assertRedirects(response, '/cart/')
        messages = list(get_messages(response.wsgi_request))     
        self.assertEqual(str(messages[0]), f"Error removing item: '{product.id}'")
