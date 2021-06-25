from django.shortcuts import (
    render, redirect, reverse,
    HttpResponse, get_object_or_404)
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Wishlist
from products.models import Product


@login_required
def view_wishlist(request):
    """ A view that renders the wishlist contents page
    """
    try:
        wishlist = get_object_or_404(Wishlist, user=request.user.id)
        wishlist_items = wishlist.products.all()
    except Exception:
        wishlist_items = ''
        messages.info(request, f'Your wishlist is empty!')

    template = 'wishlist/wishlist.html'
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, template, context)


@login_required
def add_to_wishlist(request, item_id):
    """ Add a quantity of the specified product to the shopping bag
    """
    product = get_object_or_404(Product, pk=item_id)
    try:
        wishlist = get_object_or_404(Wishlist, user=request.user.id)
        if product in wishlist.products.all():
            messages.info(request, 'That item is already in your wishlist!')
        else:
            wishlist.products.add(product)
            messages.info(request, f'Added {product.title} to your wishlist')

    except Exception:
        wishlist = Wishlist.objects.create(user=request.user)
        wishlist.products.add(product)
        messages.info(request, f'Added {product.title} to your wishlist')

    return redirect(reverse('product_detail', args=[item_id]))


@login_required
def remove_from_wishlist(request, item_id):
    """Remove the item from wishlist
    """
    try:
        product = get_object_or_404(Product, pk=item_id)
        wishlist = get_object_or_404(Wishlist, user=request.user.id)
        wishlist.products.remove(product)
        messages.info(request, f'Removed {product.title} from your wishlist')
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
