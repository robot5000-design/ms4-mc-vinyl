from django.test import TestCase

from django.contrib.auth.models import User
from .models import Wishlist


class TestWishlistModels(TestCase):
    def test_wishlist_model_string_method(self):
        testuser = User.objects.create_user(
            username='testuser', password='testpassword')
        wishlist = Wishlist.objects.create(
            user=testuser
        )
        self.assertEqual(str(wishlist), f"{wishlist.user}'s Wishlist")
