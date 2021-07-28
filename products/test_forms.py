# import datetime

# from django.test import TestCase

# from django.contrib.auth.models import User
# from products.forms import (
#     ProductForm, ProductReviewForm, GenreForm, PromotionForm)
# from products.models import Product


# class TestProductsForms(TestCase):
#     def setUp(self):
#         User.objects.create_user(
#             username='testuser', password='testpassword')
#         Product.objects.create(
#             artist='Test Artist',
#             title='Test Title',
#             sku='Test SKU',
#             price='1',
#         )

#     # Test Genre form
#     #
#     def test_genre_form_friendly_name_required(self):
#         form = GenreForm({
#             'name': 'test',
#             'friendly_name': ''
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('friendly_name', form.errors.keys())
#         self.assertEqual(form.errors['friendly_name'][0],
#                          'This field is required.')

#     def test_genre_form_name_required(self):
#         form = GenreForm({
#             'name': '',
#             'friendly_name': 'test'
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('name', form.errors.keys())
#         self.assertEqual(form.errors['name'][0], 'This field is required.')

#     def test_genre_form_name_validation_no_spaces(self):
#         form = GenreForm({
#             'name': 'te st',
#             'friendly_name': 'test',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('name', form.errors.keys())
#         self.assertEqual(form.errors['name'][0], 'Enter a valid value.')

#     def test_genre_form_name_validation_no_special_characters(self):
#         form = GenreForm({
#             'name': 'te*st',
#             'friendly_name': 'test',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('name', form.errors.keys())
#         self.assertEqual(form.errors['name'][0], 'Enter a valid value.')

#     # Test Promotion form
#     #
#     def test_promotion_form_friendly_name_required(self):
#         form = PromotionForm({
#             'name': 'test',
#             'friendly_name': ''
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('friendly_name', form.errors.keys())
#         self.assertEqual(form.errors['friendly_name'][0], 'This field is required.')

#     def test_promotion_form_name_required(self):
#         form = PromotionForm({
#             'name': '',
#             'friendly_name': 'test'
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('name', form.errors.keys())
#         self.assertEqual(form.errors['name'][0], 'This field is required.')

#     def test_promotion_form_name_validation_no_spaces(self):
#         form = PromotionForm({
#             'name': 'te st',
#             'friendly_name': 'test',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('name', form.errors.keys())
#         self.assertEqual(form.errors['name'][0], 'Enter a valid value.')

#     def test_promotion_form_name_validation_no_special_characters(self):
#         form = PromotionForm({
#             'name': 'te*st',
#             'friendly_name': 'test',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('name', form.errors.keys())
#         self.assertEqual(form.errors['name'][0], 'Enter a valid value.')

#     # Test Product Form
#     #
#     def test_add_edit_product_form_artist_required(self):
#         form = ProductForm({
#             'artist': '',
#             'title': 'test',
#             'sku': 'test',
#             'price': '1',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('artist', form.errors.keys())
#         self.assertEqual(form.errors['artist'][0], 'This field is required.')

#     def test_add_edit_product_form_title_required(self):
#         form = ProductForm({
#             'artist': 'test',
#             'title': '',
#             'sku': 'test',
#             'price': '1',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('title', form.errors.keys())
#         self.assertEqual(form.errors['title'][0], 'This field is required.')

#     def test_add_edit_product_form_sku_required(self):
#         form = ProductForm({
#             'artist': 'test',
#             'title': 'test',
#             'sku': '',
#             'price': '1',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('sku', form.errors.keys())
#         self.assertEqual(form.errors['sku'][0], 'This field is required.')

#     def test_add_edit_product_form_price_required(self):
#         form = ProductForm({
#             'artist': 'test',
#             'title': 'test',
#             'sku': 'test',
#             'price': '',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('price', form.errors.keys())
#         self.assertEqual(form.errors['price'][0], 'This field is required.')

#     def test_add_edit_product_form_price_must_be_integer(self):
#         form = ProductForm({
#             'artist': 'test',
#             'title': 'test',
#             'sku': 'test',
#             'price': 'test',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('price', form.errors.keys())
#         self.assertEqual(form.errors['price'][0], 'Enter a number.')

#     def test_add_edit_product_form_release_date_invalid_date(self):
#         form = ProductForm({
#             'artist': 'test',
#             'title': 'test',
#             'sku': 'test',
#             'price': '1',
#             'release_date': '1800'
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('release_date', form.errors.keys())
#         self.assertEqual(form.errors[
#             'release_date'][0],
#             f'Year in format YYYY between 1900-{datetime.datetime.now().year}')

#     def test_add_edit_product_form_release_date_valid_date(self):
#         form = ProductForm({
#             'artist': 'test',
#             'title': 'test',
#             'sku': 'test',
#             'price': '1',
#             'release_date': '1900'
#             })
#         self.assertTrue(form.is_valid())

#     def test_add_edit_product_form_rating_invalid_entry(self):
#         form = ProductForm({
#             'artist': 'test',
#             'title': 'test',
#             'sku': 'test',
#             'price': '1',
#             'rating': '6'
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('rating', form.errors.keys())
#         self.assertEqual(form.errors[
#             'rating'][0], 'Number between 0 & 5')

#     def test_add_edit_product_form_rating_valid_entry(self):
#         form = ProductForm({
#             'artist': 'test',
#             'title': 'test',
#             'sku': 'test',
#             'price': '1',
#             'rating': '0'
#             })
#         self.assertTrue(form.is_valid())

#     # Test Product Review Form
#     #
#     def test_review_form_body_required(self):
#         testuser_1 = User.objects.get(username='testuser')
#         product = Product.objects.get(sku='Test SKU')
#         form = ProductReviewForm({
#             'product': product,
#             'user': testuser_1,
#             'body': '',
#             'review_rating': '5',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('body', form.errors.keys())
#         self.assertEqual(form.errors['body'][0], 'This field is required.')

#     def test_review_form_rating_required(self):
#         testuser_1 = User.objects.get(username='testuser')
#         product = Product.objects.get(sku='Test SKU')
#         form = ProductReviewForm({
#             'product': product,
#             'user': testuser_1,
#             'body': 'test body',
#             'review_rating': '',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('review_rating', form.errors.keys())
#         self.assertEqual(form.errors['review_rating'][0],
#         'This field is required.')

#     def test_review_form_rating_invalid_entry(self):
#         testuser_1 = User.objects.get(username='testuser')
#         product = Product.objects.get(sku='Test SKU')
#         form = ProductReviewForm({
#             'product': product,
#             'user': testuser_1,
#             'body': 'test body',
#             'review_rating': '0',
#             })
#         self.assertFalse(form.is_valid())
#         self.assertIn('review_rating', form.errors.keys())
#         self.assertEqual(form.errors[
#             'review_rating'][0],
#             'Select a valid choice. 0 is not one of the available choices.')

#     def test_review_form_rating_valid_entry(self):
#         testuser_1 = User.objects.get(username='testuser')
#         product = Product.objects.get(sku='Test SKU')
#         form = ProductReviewForm({
#             'product': product,
#             'user': testuser_1,
#             'body': 'test body',
#             'review_rating': '5',
#             })
#         self.assertTrue(form.is_valid())
