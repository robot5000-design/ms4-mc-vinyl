from django.test import TestCase

from django.contrib.auth.models import User
from .models import Product, ProductReview, Genre, Promotion


class TestProductsModels(TestCase):
    def setUp(self):
        testuser = User.objects.create_user(
            username='testuser', password='testpassword')

        Genre.objects.create(
            name='test-genre', friendly_name='test genre')

        Promotion.objects.create(
            name='test-promotion', friendly_name='test promotion')
        
        product = Product.objects.create(
            artist='Test Artist',
            title='Test Title',
            sku='Test SKU',
            price='1',
        )

        ProductReview.objects.create(
            product=product,
            user=testuser,
            body='Test body',
            review_rating=5,
        )

    def test_genre_string_method(self):
        genre = Genre.objects.get(name='test-genre')
        self.assertEqual(str(genre), genre.name)
        self.assertEqual(genre.get_friendly_name(), genre.friendly_name)

    def test_promotion_string_method(self):
        promotion = Promotion.objects.get(name='test-promotion')
        self.assertEqual(str(promotion), promotion.name)
        self.assertEqual(promotion.get_friendly_name(), promotion.friendly_name)

    def test_product_string_method(self):
        product = Product.objects.get(sku='Test SKU')
        self.assertEqual(str(product), product.sku)

    def test_product_review_string_method(self):
        product = Product.objects.get(sku='Test SKU')
        review = ProductReview.objects.get(product=product)
        self.assertEqual(
            str(review),
            f'{review.product.title} - {review.user.username} - {review.review_rating}'
        )
