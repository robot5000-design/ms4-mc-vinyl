import datetime
from django.db import models
from django.core.validators import (
    MaxValueValidator, MinValueValidator, RegexValidator)
from django_better_admin_arrayfield.models.fields import ArrayField
from django.db.models import Avg
from django.contrib.auth.models import User


def current_year():
    ''' Returns current year as an integer
    '''
    todays_date = datetime.datetime.now()
    return todays_date.year


class Genre(models.Model):
    ''' Represents a genre field.
    '''
    name = models.CharField(
        max_length=50, validators=[RegexValidator(regex='^[-a-z0-9_]+$')])
    friendly_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Promotion(models.Model):
    ''' Represents a promotions field.
    '''
    name = models.CharField(
        max_length=50, validators=[RegexValidator(regex='^[-a-z0-9_]+$')])
    friendly_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    ''' Represents a product and its details.
    '''
    artist = models.CharField(max_length=254)
    label = models.CharField(max_length=254, blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    promotion = models.ManyToManyField(Promotion, blank=True)
    sku = models.CharField(max_length=254)
    title = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    release_date = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(
                current_year(),
                message=f'Year in format YYYY between 1900-{current_year()}'),
            MinValueValidator(
                1900,
                message=f'Year in format YYYY between 1900-{current_year()}')]
        )
    album_format = models.CharField(max_length=40, blank=True)
    color = models.CharField(max_length=15, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pre_discount_price = models.DecimalField(max_digits=6, decimal_places=2,
                                             null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1,
                                 null=True, blank=True,
                                 validators=[MaxValueValidator(5,
                                             message='Number between 0 & 5'),
                                             MinValueValidator(0,
                                             message='Number between 0 & 5')
                                             ])
    image = models.ImageField(null=True, blank=True)
    track_list = ArrayField(
        models.CharField(max_length=100, blank=True),
        default=list,
        blank=True
    )

    def calculate_rating(self):
        ''' Calculates the product rating
        '''
        self.rating = self.reviews.aggregate(
            Avg('review_rating'))['review_rating__avg']
        self.save()

    def __str__(self):
        return self.sku


class ProductReview(models.Model):
    ''' Represents a product review table.
    '''
    REVIEW_RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    body = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    review_rating = models.IntegerField(choices=REVIEW_RATING_CHOICES,
                                        default=None)
    upvote_list = models.ManyToManyField(User, blank=True,
                                         related_name='upvote_users')
    upvote_count = models.IntegerField(default=0)
    admin_comment = models.TextField(blank=True)

    class Meta:
        ''' Default ordering for product reviews.
        '''
        ordering = ["-review_date"]

    def __str__(self):
        return f'{self.product.title} - {self.user.username} - {self.review_rating}'
