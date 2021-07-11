from django.db import models

from products.models import Product
from django.contrib.auth.models import User


class Wishlist(models.Model):
    products = models.ManyToManyField(Product, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s Wishlist"
