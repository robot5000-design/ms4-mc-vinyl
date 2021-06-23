import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django_better_admin_arrayfield.models.fields import ArrayField
from django.db.models import Avg
from django.contrib.auth.models import User


def current_year():
    ''' Returns current year as an integer
    '''
    todays_date = datetime.datetime.now()
    return todays_date.year


class Genre(models.Model):
    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    artist = models.CharField(max_length=254)
    label = models.CharField(max_length=254, blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    sku = models.CharField(max_length=254)
    title = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    release_date = models.IntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(
            current_year(), message='Year in format YYYY'),
            MinValueValidator(1900, message='Year in format YYYY')]
        )
    album_format = models.CharField(max_length=40, blank=True)
    color = models.CharField(max_length=15, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1,
                                 null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    track_list = ArrayField(
        models.CharField(max_length=100, blank=True),
        default=list,
        blank=True
    )

    def calculate_rating(self):
        self.rating = self.reviews.aggregate(
            Avg('review_rating'))['review_rating__avg']
        self.save()

    def __str__(self):
        return f'{self.title} - {self.artist}'


class ProductReview(models.Model):
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
    review_date = models.DateTimeField(auto_now=True)
    review_rating = models.IntegerField(choices=REVIEW_RATING_CHOICES,
                                        default=None)
    upvote_list = ArrayField(
        models.CharField(max_length=100, blank=True),
        default=list,
        blank=True
    )
    admin_comment = models.TextField(blank=True)

    def __str__(self):
        return f'{self.product.title} - {self.user.username} - {self.review_rating}'
