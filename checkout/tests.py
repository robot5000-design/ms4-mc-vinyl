from django.test import TestCase


class TestCheckoutForms(TestCase):
    # def setUp(self):
    #     User.objects.create_user(
    #         username='testuser', password='testpassword')
    #     Product.objects.create(
    #         artist='Test Artist',
    #         title='Test Title',
    #         sku='Test SKU',
    #         price='1',
    #     )

    Test Order form
    
    def test_order_form_friendly_name_required(self):
        form = GenreForm({
            'name': 'test',
            'friendly_name': ''
            })
        self.assertFalse(form.is_valid())
        self.assertIn('friendly_name', form.errors.keys())
        self.assertEqual(form.errors['friendly_name'][0],
                         'This field is required.')

