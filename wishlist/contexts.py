from django.shortcuts import get_object_or_404

from .models import Wishlist


def wishlist_contents(request):
    ''' Wishlist context to display number of items in the navbar
    '''
    try:
        wishlist = get_object_or_404(Wishlist, user=request.user.id)
        wishlist_items = wishlist.products.all()
        wishlist_count = len(wishlist_items)
    except Exception:
        wishlist_count = None

    context = {
        'wishlist_count': wishlist_count,
    }

    return context
