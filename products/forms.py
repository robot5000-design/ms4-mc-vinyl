from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Genre


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'artist',
            'title',
            'release_date',
            'sku',
            'price',
            'genre',
            'description',           
            'album_format',
            'color',
            'rating',
            'image',
            'track_list',
            )

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        genres = Genre.objects.all()
        genres_friendly_names = [(genre.id, genre.get_friendly_name()) for genre in genres]
        self.fields['genre'].choices = genres_friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
