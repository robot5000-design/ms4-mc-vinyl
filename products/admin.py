from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import Product, Genre, ProductReview


class ProductAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = (
        'title',
        'artist',
        'sku',
        'color',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
    )


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        'body',
        'review_rating',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Genre, GenreAdmin)
