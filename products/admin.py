from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import Album, Artist, Label, Genre


class AlbumAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = (
        'sku',
        'title',
        'artist',
        'color',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class LabelAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Genre, GenreAdmin)
