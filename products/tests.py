from django.test import TestCase
from products.models import Product, ProductReview, Genre, Promotion
from products.forms import ProductForm

from django.contrib.auth.models import AnonymousUser, User



class TestViews(TestCase):

    def test_get_all_products(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_blank_search_all_products(self):
        response = self.client.get('/products/', {'q': ''})
        self.assertRedirects(response, '/products/')

    def test_get_product_detail(self):
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        response = self.client.get(f'/products/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    # Test Edit Product Function
    #     
    def test_edit_product(self):
        test_user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        response = self.client.post(f'/products/edit/{product.id}/', {
            'artist': 'Updated Artist',
            'title': 'Test Title',
            'sku': 'Test SKU',
            'price': '1',
        })
        self.assertRedirects(response, f'/products/{product.id}/')
        updated_item = Product.objects.get(id=product.id)
        self.assertEqual(updated_item.artist, 'Updated Artist')

    def test_login_required_for_edit_product(self):
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        response = self.client.post(f'/products/edit/{product.id}/', {
            'artist': 'Updated Artist',
            'title': 'Test Title',
            'sku': 'Test SKU',
            'price': '1',
        })
        self.assertRedirects(response, f'/accounts/login/?next=/products/edit/{product.id}/')

    def test_superuser_required_for_edit_product(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        response = self.client.post(f'/products/edit/{product.id}/', {
            'artist': 'Updated Artist',
            'title': 'Test Title',
            'sku': 'Test SKU',
            'price': '1',
        })
        self.assertRedirects(response, '/')

    # Test Add Product Function
    
    def test_add_product(self):
        test_user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/products/add/', {
            'artist': 'Test Artist',
            'title': 'Test Title',
            'sku': 'Test SKU',
            'price': '1',
        })
        product = Product.objects.get(sku='Test SKU')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_login_required_for_add_product(self):
        response = self.client.post('/products/add/', {
            'artist': 'Test Artist',
            'title': 'Test Title',
            'sku': 'Test SKU',
            'price': '1',
        })
        self.assertRedirects(response, '/accounts/login/?next=/products/add/')

    def test_superuser_required_for_add_product(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/products/add/', {
            'artist': 'Test Artist',
            'title': 'Test Title',
            'sku': 'Test SKU',
            'price': '1',
        })
        self.assertRedirects(response, '/')

    # Test Delete Product Function
    #
    def test_delete_product(self):
        test_user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        response = self.client.post(f'/products/delete/{product.id}/')
        self.assertRedirects(response, '/products/')
        deleted_item = Product.objects.filter(id=product.id)
        self.assertEqual(len(deleted_item), 0)

    def test_login_required_for_delete_product(self):
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        response = self.client.post(f'/products/delete/{product.id}/')
        self.assertRedirects(response, f'/accounts/login/?next=/products/delete/{product.id}/')

    def test_superuser_required_for_delete_product(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        response = self.client.post(f'/products/delete/{product.id}/')
        self.assertRedirects(response, '/')

    # Test Add Product Review Function
    
    def test_add_product_review(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        response = self.client.post(f'/products/add_review/{product.id}/', {
            'body': 'Test body',
            'review_rating': 5,
        })
        review = ProductReview.objects.get(product=product, user=test_user, body='Test body')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_login_required_add_product_review(self):
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        response = self.client.post(f'/products/add_review/{product.id}/', {
            'body': 'Test body',
            'review_rating': 5,
        })
        self.assertRedirects(response, f'/accounts/login/?next=/products/add_review/{product.id}/')
        review = ProductReview.objects.filter(product=product, body='Test body')
        self.assertEqual(len(review), 0)

    def test_edit_product_review(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        self.client.post(f'/products/add_review/{product.id}/', {
            'product': product,
            'user': test_user,
            'body': 'Test body',
            'review_rating': 5,
        })
        response = self.client.post(f'/products/edit_review/{product.id}/{test_user.username}/', {
            'body': 'Updated body',
            'review_rating': 1,
        })
        review = ProductReview.objects.get(product=product, review_rating=1)
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_user_cannot_edit_another_users_review(self):
        test_user_1 = User.objects.create_user(username='testuser1', password='testpassword')
        test_user_2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.client.login(username='testuser1', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        self.client.post(f'/products/add_review/{product.id}/', {
            'body': 'Test body',
            'review_rating': 5,
        })
        self.client.logout()
        self.client.login(username='testuser2', password='testpassword')
        ProductReview.objects.get(product=product, review_rating=5)
        response = self.client.post(f'/products/edit_review/{product.id}/{test_user_1.username}/', {
            'body': 'Updated body',
            'review_rating': 1,
        })
        self.assertRedirects(response, '/')
        ProductReview.objects.get(product=product, review_rating=5)


    def test_superuser_can_edit_another_users_review(self):
        test_user_1 = User.objects.create_user(username='testuser1', password='testpassword')
        test_user_2 = User.objects.create_superuser(username='testuser2', password='testpassword')
        self.client.login(username='testuser1', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        self.client.post(f'/products/add_review/{product.id}/', {
            'body': 'Test body',
            'review_rating': 5,
        })
        self.client.logout()
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.post(f'/products/edit_review/{product.id}/{test_user_1.username}/', {
            'body': 'Updated body',
            'review_rating': 1,
        })
        review = ProductReview.objects.get(product=product, review_rating=1)
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_delete_product_review(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        self.client.post(f'/products/add_review/{product.id}/', {
            'body': 'Test body',
            'review_rating': 5,
        })
        ProductReview.objects.get(product=product, review_rating=5)
        response = self.client.post(f'/products/delete_review/{product.id}/{test_user.username}/')
        self.assertRedirects(response, f'/products/{product.id}/')
        review = ProductReview.objects.filter(product=product, review_rating=5)
        self.assertEqual(len(review), 0)

    def test_user_cannot_delete_another_users_review(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        test_user_2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        self.client.post(f'/products/add_review/{product.id}/', {
            'body': 'Test body',
            'review_rating': 5,
        })
        self.client.logout()
        ProductReview.objects.get(product=product, review_rating=5)
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.post(f'/products/delete_review/{product.id}/{test_user.username}/')
        self.assertRedirects(response, '/')
        ProductReview.objects.get(product=product, review_rating=5)

    def test_superuser_can_delete_another_users_review(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        test_user_2 = User.objects.create_superuser(username='testuser2', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        self.client.post(f'/products/add_review/{product.id}/', {
            'body': 'Test body',
            'review_rating': 5,
        })
        self.client.logout()
        ProductReview.objects.get(product=product, review_rating=5)
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.post(f'/products/delete_review/{product.id}/{test_user.username}/')
        self.assertRedirects(response, f'/products/{product.id}/')
        review = ProductReview.objects.filter(product=product, review_rating=5)
        self.assertEqual(len(review), 0)

    def test_upvote_product_review(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        test_user_2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        review = ProductReview.objects.create(
            product=product,
            user=test_user,
            body='Test body',
            review_rating=5,
        )
        ProductReview.objects.get(product=product, review_rating=5)
        self.client.logout()
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.post(f'/products/upvote_review/{product.id}/{test_user.username}/')
        self.assertEqual(response.status_code, 200)
        review = ProductReview.objects.get(product=product, review_rating=5)
        review.upvote_list.get(id=test_user_2.id)

    def test_cannot_upvote_own_review(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )
        review = ProductReview.objects.create(
            product=product,
            user=test_user,
            body='Test body',
            review_rating=5,
        )
        ProductReview.objects.get(product=product, review_rating=5)
        response = self.client.post(f'/products/upvote_review/{product.id}/{test_user.username}/')
        self.assertEqual(response.status_code, 200)
        review = ProductReview.objects.get(product=product, review_rating=5)
        user = review.upvote_list.filter(id=test_user.id)
        self.assertEqual(len(user), 0)

    def test_add_product_tag_genre(self):
        test_user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/products/product_tags_admin/', {
            'genre': '',
            'name': 'pop',
            'friendly_name': 'Pop',
        })
        self.assertRedirects(response, '/products/product_tags_admin/')
        Genre.objects.get(name='pop')

    def test_add_product_tag_promotion(self):
        test_user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/products/product_tags_admin/', {
            'promotion': '',
            'name': 'sale',
            'friendly_name': 'Sale',
        })
        self.assertRedirects(response, '/products/product_tags_admin/')
        Promotion.objects.get(name='sale')

    def test_superuser_required_add_product_tag(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/products/product_tags_admin/', {
            'promotion': '',
            'name': 'sale',
            'friendly_name': 'Sale',
        })
        self.assertRedirects(response, '/')
        promotion = Promotion.objects.filter(name='sale')
        self.assertEqual(len(promotion), 0)

