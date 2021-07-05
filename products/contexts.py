from django.shortcuts import get_object_or_404

from .models import Genre, Promotion


def genre_promotion_fields(request):
    """ Genre and Promotion fields context to display these fields
    in the Nav dropdown
    """
    genres = Genre.objects.all().order_by('name')
    promotions = Promotion.objects.all().order_by('name')

    context = {
        'genres': genres,
        'promotions': promotions,
    }

    return context
