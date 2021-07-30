from django.test import TestCase
from django.contrib.messages import get_messages

from django.contrib.auth.models import User
from .models import Wishlist
from products.models import Product


class TestWishlistModels(TestCase):

    def setUp(self):
        testuser = User.objects.create_user(
            username='testuser', password='testpassword')

        testuser.save()

        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
    
    # Test View Wishlist Page
    #
    def test_view_wishlist_page_wishlist_empty(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/wishlist/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Your wishlist is empty!')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist/wishlist.html')

    def test_login_required_view_wishlist_page(self):
        response = self.client.get('/wishlist/')
        self.assertRedirects(response, '/accounts/login/?next=/wishlist/')

    def test_view_wishlist_page_wishlist_exists(self):
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.get(sku='Test SKU')
        test_user = User.objects.get(username='testuser')
        wishlist = Wishlist.objects.create(user=test_user)
        wishlist.products.add(product)
        response = self.client.get('/wishlist/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist/wishlist.html')
        self.assertEqual(response.context['wishlist_items'][0], product)

    # Test Add to Wishlist View
    #
    def test_add_to_wishlist(self):
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.get(sku='Test SKU')
        response = self.client.get(f'/wishlist/add/{product.id}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Added item to your wishlist')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_login_required_add_to_wishlist(self):
        product = Product.objects.get(sku='Test SKU')
        response = self.client.get(f'/wishlist/add/{product.id}/')
        self.assertRedirects(response, f'/accounts/login/?next=/wishlist/add/{product.id}/')

    def test_add_to_wishlist_product_already_in_wishlist(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        product = Product.objects.get(sku='Test SKU')
        wishlist = Wishlist.objects.create(user=test_user)
        wishlist.products.add(product)
        response = self.client.get(f'/wishlist/add/{product.id}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'That item is already in your wishlist!')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_add_to_wishlist_wishlist_full(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        wishlist = Wishlist.objects.create(user=test_user)
        product_1 = Product.objects.get(sku='Test SKU')
        for index in range(2, 12):
            product = Product.objects.create(
                artist=f'Test Artist {index}',
                title=f'Test Title {index}',
                sku=f'Test SKU {index}',
                price='1',
            )
            wishlist.products.add(product)
        response = self.client.get(f'/wishlist/add/{product_1.id}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Your wishlist is full!')
        self.assertRedirects(response, f'/products/{product_1.id}/')

    # Test Remove from Wishlist View
    #
    def test_remove_from_wishlist_redirect_from_product(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        product = Product.objects.get(sku='Test SKU')
        wishlist = Wishlist.objects.create(user=test_user)
        wishlist.products.add(product)
        redirect_from = 'product'
        response = self.client.get(
            f'/wishlist/remove/{product.id}/{redirect_from}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Removed item from your wishlist')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_remove_from_wishlist_redirect_from_wishlist(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        product = Product.objects.get(sku='Test SKU')
        wishlist = Wishlist.objects.create(user=test_user)
        wishlist.products.add(product)
        redirect_from = 'wishlist'
        response = self.client.get(
            f'/wishlist/remove/{product.id}/{redirect_from}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Removed item from your wishlist')
        self.assertRedirects(response, '/wishlist/')

    def test_remove_from_wishlist_product_not_in_wishlist(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        product = Product.objects.get(sku='Test SKU')
        wishlist = Wishlist.objects.create(user=test_user)
        redirect_from = 'wishlist'
        response = self.client.get(
            f'/wishlist/remove/{product.id}/{redirect_from}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'That product is not in your wishlist!')
        self.assertRedirects(response, '/wishlist/')

    # Test Transfer all to cart View
    #
    def test_transfer_to_cart(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        product = Product.objects.get(sku='Test SKU')
        wishlist = Wishlist.objects.create(user=test_user)
        wishlist.products.add(product)
        response = self.client.get('/wishlist/transfer/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Added all items to your cart')
        self.assertRedirects(response, '/cart/')

    def test_transfer_to_cart_wishlist_empty(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        wishlist = Wishlist.objects.create(user=test_user)
        response = self.client.get('/wishlist/transfer/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "There's nothing to add!")
        self.assertRedirects(response, '/wishlist/')
