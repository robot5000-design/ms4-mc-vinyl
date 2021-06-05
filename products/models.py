import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django_better_admin_arrayfield.models.fields import ArrayField


def current_year():
    ''' Returns current year as an integer
    '''
    todays_date = datetime.datetime.now()
    return todays_date.year


class Product(models.Model):
    artist = models.ForeignKey('Artist', on_delete=models.PROTECT)
    label = models.ForeignKey('Label', null=True, blank=True,
                              on_delete=models.SET_NULL)
    genre = models.ManyToManyField('Genre', blank=True)
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
    rating = models.DecimalField(max_digits=4, decimal_places=1, null=True,
                                 blank=True)
    image = models.ImageField(null=True, blank=True)
    track_list = ArrayField(
        models.CharField(max_length=100, blank=True),
        default=list,
        blank=True
    )

    def __str__(self):
        return self.title


class Artist(models.Model):
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Label(models.Model):
    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
