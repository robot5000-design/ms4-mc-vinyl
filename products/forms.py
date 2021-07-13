from django import forms
from django.forms import Textarea
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from .widgets import CustomClearableFileInput
from .models import Product, Genre, ProductReview, Promotion


class ProductForm(forms.ModelForm):
    """ Represents a form for submitting new products or editing existing
    ones.
    """
    class Meta:
        """ Fields to be inputs of product form.
        """
        model = Product
        fields = (
            'artist',
            'title',
            'promotion',
            'label',
            'release_date',
            'sku',
            'price',
            'genre',
            'description',
            'album_format',
            'color',
            'image',
            'track_list',
            )

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        genres = Genre.objects.all()
        genres_friendly_names = [
            (genre.id, genre.get_friendly_name()) for genre in genres]
        self.fields['genre'].choices = genres_friendly_names

        promotions = Promotion.objects.all()
        promotions_friendly_names = [
            (promotion.id, promotion.get_friendly_name())
            for promotion in promotions
            ]
        self.fields['promotion'].choices = promotions_friendly_names

        for field_name, field in self.fields.items():
            if field_name == 'track_list':
                field.widget.attrs[
                    'class'] = 'p-2 my-2 mr-2 border-dark w-100 rounded-sm'
                field.widget.attrs['aria-label'] = 'track-list-item'
            elif field_name == 'image':
                field.widget.attrs['aria-label'] = 'image-input'
            else:
                field.widget.attrs['class'] = 'border-dark'


class ProductReviewForm(forms.ModelForm):
    """ Represents a form for product reviews.
    """
    class Meta:
        """ Fields and types for product review form.
        """
        model = ProductReview
        fields = (
            'body',
            'review_rating',
            'admin_comment',
        )
        widgets = {
            'body': Textarea(attrs={'rows': 4}),
            'admin_comment': Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            InlineRadios('review_rating'),
        )
        self.fields['review_rating'].widget.attrs['required'] = True
        for field in self.fields:
            if field == 'body':
                self.fields[field].label = False
                self.fields[field].widget.attrs[
                    'placeholder'] = 'Write your review here...'
            elif field == 'review_rating':
                self.fields[field].label = "What's your rating?"
            elif field == 'admin_comment':
                self.fields[field].label = 'MC Vinyl Admin Comment:'
            self.fields[field].widget.attrs[
                'class'] = 'border-dark  profile-form-input'


class GenreForm(forms.ModelForm):
    """ Represents a form for inputting new genre types.
    """
    class Meta:
        """ Fields for genre form
        """
        model = Genre
        fields = (
            'name',
            'friendly_name',
            )


class PromotionForm(forms.ModelForm):
    """ Represents a form for inputting new promotion types.
    """
    class Meta:
        """ Fields for promotion form
        """
        model = Promotion
        fields = (
            'name',
            'friendly_name',
            )
