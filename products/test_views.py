from django.test import TestCase
from django.contrib.messages import get_messages

from django.contrib.auth.models import User
from products.models import Product, ProductReview, Genre, Promotion


class TestViews(TestCase):
    def setUp(self):
        testuser_1 = User.objects.create_user(
            username='testuser', password='testpassword')
        testuser_2 = User.objects.create_user(
            username='testuser2', password='testpassword')
        testuser_su = User.objects.create_superuser(
            username='testuser_su', password='testpassword')

        testuser_1.save()
        testuser_2.save()
        testuser_su.save()

        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )

        ProductReview.objects.create(
            product=product,
            user=testuser_2,
            body='Test body',
            review_rating=5,
        )

    def tearDown(self):
        Product.objects.all().delete()
        ProductReview.objects.all().delete()

    def test_get_all_products(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_blank_search_all_products(self):
        response = self.client.get('/products/', {'q': ''})
        self.assertRedirects(response, '/products/')

    def test_get_product_detail(self):
        product = Product.objects.get()
        response = self.client.get(f'/products/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    # Test Edit Product Function
    #
    def test_get_edit_product_page(self):
        self.client.login(username='testuser_su', password='testpassword')
        product = Product.objects.get()
        response = self.client.get(f'/products/edit/{product.id}/')
        self.assertTemplateUsed(response, 'products/edit_product.html')

    def test_edit_product(self):
        self.client.login(username='testuser_su', password='testpassword')
        product = Product.objects.get()
        response = self.client.post(f'/products/edit/{product.id}/', {
            'artist': 'Updated Artist',
            'title': 'Test Title',
            'sku': 'Test SKU',
            'price': '1',
        })
        self.assertRedirects(response, f'/products/{product.id}/')
        updated_item = Product.objects.get()
        self.assertEqual(updated_item.artist, 'Updated Artist')

    def test_edit_product_sku_already_exists(self):
        self.client.login(username='testuser_su', password='testpassword')
        new_product = Product.objects.create(
            artist='Test Artist 2',
            title='Test Title 2',
            sku='Test SKU 2',
            price='1',
        )
        # try renaming new_product sku to existing product sku
        response = self.client.post(f'/products/edit/{new_product.id}/', {
            'artist': 'Test Artist 2',
            'title': 'Test Title 2',
            'sku': 'Test SKU',
            'price': '1',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'Another title with that SKU already exists!')

    def test_login_required_for_edit_product(self):
        product = Product.objects.get()
        response = self.client.post(f'/products/edit/{product.id}/', {
            'artist': 'Updated Artist',
            'title': 'Test Title',
            'sku': 'Test SKU',
            'price': '1',
        })
        self.assertRedirects(
            response, f'/accounts/login/?next=/products/edit/{product.id}/')

    def test_superuser_required_for_edit_product(self):
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.get()
        response = self.client.post(f'/products/edit/{product.id}/', {
            'artist': 'Updated Artist',
            'title': 'Test Title',
            'sku': 'Test SKU',
            'price': '1',
        })
        self.assertRedirects(response, '/')
        updated_item = Product.objects.get()
        self.assertNotEqual(updated_item.artist, 'Updated Artist')

    # Test Add Product Function
    #
    def test_get_add_product_page(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.get('/products/add/')
        self.assertTemplateUsed(response, 'products/add_product.html')

    def test_add_product(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.post('/products/add/', {
            'artist': 'Test Artist 2',
            'title': 'Test Title 2',
            'sku': 'Test SKU 2',
            'price': '1',
        })
        product = Product.objects.get(sku='Test SKU 2')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_add_product_sku_already_exists(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.post('/products/add/', {
            'artist': 'Test Artist 2',
            'title': 'Test Title 2',
            'sku': 'Test SKU',
            'price': '1',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 'That SKU already exists!')

    def test_login_required_for_add_product(self):
        response = self.client.post('/products/add/', {
            'artist': 'Test Artist 2',
            'title': 'Test Title 2',
            'sku': 'Test SKU 2',
            'price': '1',
        })
        self.assertRedirects(response, '/accounts/login/?next=/products/add/')
        product = Product.objects.filter(artist='Test Artist 2')
        self.assertEqual(len(product), 0)

    def test_superuser_required_for_add_product(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/products/add/', {
            'artist': 'Test Artist 2',
            'title': 'Test Title 2',
            'sku': 'Test SKU 2',
            'price': '1',
        })
        self.assertRedirects(response, '/')
        product = Product.objects.filter(artist='Test Artist 2')
        self.assertEqual(len(product), 0)


class TestViews2(TestCase):
    def setUp(self):
        testuser_1 = User.objects.create_user(
            username='testuser', password='testpassword')
        testuser_2 = User.objects.create_user(
            username='testuser2', password='testpassword')
        testuser_su = User.objects.create_superuser(
            username='testuser_su', password='testpassword')

        testuser_1.save()
        testuser_2.save()
        testuser_su.save()

        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )

        ProductReview.objects.create(
            product=product,
            user=testuser_2,
            body='Test body',
            review_rating=5,
        )

    def tearDown(self):
        Product.objects.all().delete()
        ProductReview.objects.all().delete()

    # Test Delete Product Function
    #
    def test_delete_product(self):
        self.client.login(username='testuser_su', password='testpassword')
        product = Product.objects.get()
        response = self.client.post(f'/products/delete/{product.id}/')
        self.assertRedirects(response, '/products/')
        deleted_item = Product.objects.filter(id=product.id)
        self.assertEqual(len(deleted_item), 0)

    def test_delete_product_post_method_required(self):
        self.client.login(username='testuser_su', password='testpassword')
        product = Product.objects.get()
        response = self.client.get(f'/products/delete/{product.id}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid Method.')
        self.assertRedirects(response, '/products/')

    def test_login_required_for_delete_product(self):
        product = Product.objects.get()
        response = self.client.post(f'/products/delete/{product.id}/')
        self.assertRedirects(response, f'/accounts/login/?next=/products/delete/{product.id}/')
        Product.objects.get(id=product.id)

    def test_superuser_required_for_delete_product(self):
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.get()
        response = self.client.post(f'/products/delete/{product.id}/')
        self.assertRedirects(response, '/')
        Product.objects.get(id=product.id)

    # Test Add Product Review Function
    #
    def test_add_product_review(self):
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.get()
        response = self.client.post(f'/products/add_review/{product.id}/', {
            'body': 'Test body new',
            'review_rating': 1,
        })
        ProductReview.objects.get(product=product, body='Test body new')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_add_product_review_already_reviewed(self):
        self.client.login(username='testuser2', password='testpassword')
        product = Product.objects.get()
        user = User.objects.get(username='testuser2')
        ProductReview.objects.get(product=product, user=user)
        response = self.client.post(f'/products/add_review/{product.id}/', {
            'body': 'Test body new',
            'review_rating': 1,
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Already reviewed!')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_add_product_review_post_method_required(self):
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.get()
        response = self.client.get(f'/products/add_review/{product.id}/', {
            'body': 'Test body new',
            'review_rating': 5,
        })
        review = ProductReview.objects.filter(
            product=product, body='Test body new')
        self.assertEqual(len(review), 0)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid Method.')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_login_required_add_product_review(self):
        product = Product.objects.get()
        response = self.client.post(f'/products/add_review/{product.id}/', {
            'body': 'Test body 2',
            'review_rating': 1,
        })
        self.assertRedirects(response, f'/accounts/login/?next=/products/add_review/{product.id}/')
        review = ProductReview.objects.filter(product=product,
                                              body='Test body 2')
        self.assertEqual(len(review), 0)

    def test_get_edit_product_review_page(self):
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.get()
        user = User.objects.get(username='testuser')
        self.client.post(f'/products/add_review/{product.id}/', {
            'product': product,
            'user': user,
            'body': 'Test body 2',
            'review_rating': 1,
        })
        response = self.client.get(
            f'/products/edit_review/{product.id}/{user.username}/')
        self.assertTemplateUsed(response, 'products/edit_product_review.html')

    def test_edit_product_review(self):
        self.client.login(username='testuser2', password='testpassword')
        product = Product.objects.get()
        user = User.objects.get(username='testuser2')
        response = self.client.post(
            f'/products/edit_review/{product.id}/{user.username}/', {
             'body': 'Updated body',
             'review_rating': 1,
             })
        ProductReview.objects.get(product=product, body='Updated body')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_add_admin_comment_to_review(self):
        self.client.login(username='testuser_su', password='testpassword')
        product = Product.objects.get()
        user = User.objects.get(username='testuser2')
        response = self.client.post(
            f'/products/edit_review/{product.id}/{user.username}/', {
             'admin_comment': 'admin test comment',
             'body': 'Updated body',
             'review_rating': 1,
             })
        ProductReview.objects.get(
            product=product, admin_comment='admin test comment')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_user_cannot_edit_another_users_review(self):
        self.client.login(username='testuser', password='testpassword')
        test_user_2 = User.objects.get(username='testuser2')
        product = Product.objects.get()
        response = self.client.post(
            f'/products/edit_review/{product.id}/{test_user_2.username}/', {
             'body': 'Updated body',
             'review_rating': 1,
             })
        self.assertRedirects(response, '/')
        review = ProductReview.objects.filter(product=product,
                                              body='Updated body')
        self.assertEqual(len(review), 0)
        ProductReview.objects.get(product=product, body='Test body')

    def test_superuser_can_edit_another_users_review(self):
        self.client.login(username='testuser_su', password='testpassword')
        product = Product.objects.get()
        test_user_2 = User.objects.get(username='testuser2')
        response = self.client.post(
            f'/products/edit_review/{product.id}/{test_user_2.username}/', {
             'body': 'Updated body',
             'review_rating': 1,
             })
        ProductReview.objects.get(product=product, body='Updated body')
        self.assertRedirects(response, f'/products/{product.id}/')

    def test_delete_product_review(self):
        self.client.login(username='testuser2', password='testpassword')
        test_user_2 = User.objects.get(username='testuser2')
        product = Product.objects.get()
        response = self.client.post(
            f'/products/delete_review/{product.id}/{test_user_2.username}/')
        self.assertRedirects(response, f'/products/{product.id}/')
        review = ProductReview.objects.filter(product=product,
                                              body='Test body')
        self.assertEqual(len(review), 0)

    def test_delete_product_review_post_method_required(self):
        self.client.login(username='testuser2', password='testpassword')
        test_user_2 = User.objects.get(username='testuser2')
        product = Product.objects.get()
        response = self.client.get(
            f'/products/delete_review/{product.id}/{test_user_2.username}/')
        self.assertRedirects(response, f'/products/{product.id}/')
        ProductReview.objects.get(product=product, body='Test body')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid Method.')

    def test_user_cannot_delete_another_users_review(self):
        self.client.login(username='testuser', password='testpassword')
        test_user_2 = User.objects.get(username='testuser2')
        product = Product.objects.get()
        response = self.client.post(
            f'/products/delete_review/{product.id}/{test_user_2.username}/')
        self.assertRedirects(response, '/')
        ProductReview.objects.get(product=product, body='Test body')

    def test_superuser_can_delete_another_users_review(self):
        self.client.login(username='testuser_su', password='testpassword')
        test_user_2 = User.objects.get(username='testuser2')
        product = Product.objects.get()
        response = self.client.post(
            f'/products/delete_review/{product.id}/{test_user_2.username}/')
        self.assertRedirects(response, f'/products/{product.id}/')
        review = ProductReview.objects.filter(product=product,
                                              body='Test body')
        self.assertEqual(len(review), 0)


class TestViews3(TestCase):
    def setUp(self):
        testuser_1 = User.objects.create_user(
            username='testuser', password='testpassword')
        testuser_2 = User.objects.create_user(
            username='testuser2', password='testpassword')
        testuser_su = User.objects.create_superuser(
            username='testuser_su', password='testpassword')

        testuser_1.save()
        testuser_2.save()
        testuser_su.save()

        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )

        ProductReview.objects.create(
            product=product,
            user=testuser_2,
            body='Test body',
            review_rating=5,
        )

    def tearDown(self):
        Product.objects.all().delete()
        ProductReview.objects.all().delete()

    # Test Review Upvotes
    #
    def test_upvote_product_review(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        test_user_2 = User.objects.get(username='testuser2')
        product = Product.objects.get()
        response = self.client.post(
            f'/products/upvote_review/{product.id}/{test_user_2.username}/')
        self.assertEqual(response.status_code, 200)
        review = ProductReview.objects.get(product=product, body='Test body')
        user = review.upvote_list.filter(id=test_user.id)
        self.assertEqual(len(user), 1)

    def test_cannot_upvote_own_review(self):
        self.client.login(username='testuser2', password='testpassword')
        test_user_2 = User.objects.get(username='testuser2')
        product = Product.objects.get()
        response = self.client.post(
            f'/products/upvote_review/{product.id}/{test_user_2.username}/')
        self.assertEqual(response.status_code, 200)
        review = ProductReview.objects.get(product=product, body='Test body')
        user = review.upvote_list.filter(id=test_user_2.id)
        self.assertEqual(len(user), 0)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "You can't like your own review!!")

    def test_already_upvoted_this_review(self):
        self.client.login(username='testuser', password='testpassword')
        test_user = User.objects.get(username='testuser')
        test_user_2 = User.objects.get(username='testuser2')
        product = Product.objects.get()
        self.client.post(
            f'/products/upvote_review/{product.id}/{test_user_2.username}/')
        review = ProductReview.objects.get(product=product, body='Test body')
        review.upvote_list.get(id=test_user.id)
        response = self.client.post(
            f'/products/upvote_review/{product.id}/{test_user_2.username}/')
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'Already Liked!')

    # Test Add Product Tags Function

    def test_get_add_product_tags_page(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.get('/products/product_tags_admin/')
        self.assertTemplateUsed(response, 'products/product_tags_admin.html')

    def test_add_product_tag_genre(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.post('/products/product_tags_admin/', {
            'genre': '',
            'name': 'pop',
            'friendly_name': 'Pop',
        })
        self.assertRedirects(response, '/products/product_tags_admin/')
        Genre.objects.get(name='pop')

    def test_add_product_tag_genre_already_exists(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.post('/products/product_tags_admin/', {
            'genre': '',
            'name': 'pop',
            'friendly_name': 'Pop',
        })
        self.assertRedirects(response, '/products/product_tags_admin/')
        Genre.objects.get(name='pop')
        response = self.client.post('/products/product_tags_admin/', {
            'genre': '',
            'name': 'pop',
            'friendly_name': 'Pop',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Genre already exists!')

    def test_add_product_tag_promotion(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.post('/products/product_tags_admin/', {
            'promotion': '',
            'name': 'sale',
            'friendly_name': 'Sale',
        })
        self.assertRedirects(response, '/products/product_tags_admin/')
        Promotion.objects.get(name='sale')

    def test_add_product_tag_promotion_already_exists(self):
        self.client.login(username='testuser_su', password='testpassword')
        response = self.client.post('/products/product_tags_admin/', {
            'promotion': '',
            'name': 'sale',
            'friendly_name': 'Sale',
        })
        self.assertRedirects(response, '/products/product_tags_admin/')
        Promotion.objects.get(name='sale')
        response = self.client.post('/products/product_tags_admin/', {
            'promotion': '',
            'name': 'sale',
            'friendly_name': 'Sale',
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Promotion already exists!')

    def test_superuser_required_add_product_tag(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/products/product_tags_admin/', {
            'promotion': '',
            'name': 'sale',
            'friendly_name': 'Sale',
        })
        self.assertRedirects(response, '/')
        promotion = Promotion.objects.filter(name='sale')
        self.assertEqual(len(promotion), 0)
