from django.shortcuts import (
    render, redirect, reverse,
    get_object_or_404)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404

from products.models import Product
from .models import Wishlist


@login_required
def view_wishlist(request):
    ''' A view that renders the wishlist contents page.

    Args:
        request (object): HTTP request object.
    Returns:
        Renders the wishlist page.
    '''
    try:
        wishlist = Wishlist.objects.filter(user=request.user.id)[0]

    except IndexError:
        wishlist_items = None
    else:
        wishlist_items = wishlist.products.all()

    if not wishlist_items:
        messages.info(request, 'Your wishlist is empty!')

    template = 'wishlist/wishlist.html'
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, template, context)


@login_required
def add_to_wishlist(request, item_id):
    ''' Add a quantity of the specified product to the wishlist.

    Checks if the product and the wishlist exist. If the wishlist does
    not exist, it is created and the product is added to it. The wishlist
    is set to allow a maximum of 10 products.

    Args:
        request (object): HTTP request object.
        item_id (int): id which identifies a product in the database.
    Returns:
        Redirects to the product detail page for that product.
    '''
    product = get_object_or_404(Product, pk=item_id)

    try:
        wishlist = get_object_or_404(Wishlist, user=request.user.id)
    except Http404:
        wishlist = Wishlist.objects.create(user=request.user)

    if wishlist.products.all().count() > 9:
        messages.info(request, 'Your wishlist is full!')
    elif product in wishlist.products.all():
        messages.info(request, 'That item is already in your wishlist!')
    else:
        wishlist.products.add(product)
        messages.info(request, 'Added item to your wishlist')

    return redirect(reverse('product_detail', args=[item_id]))


@login_required
def remove_from_wishlist(request, item_id, redirect_from):
    '''Remove the item from wishlist.

    Gets the product and wishlist from the database and removes the
    product from the request user's wishlist if it exists.

    Args:
        request (object): HTTP request object.
        item_id (int): id which identifies a product in the database.
    Returns:
        Redirects to the wishlist page.
    '''
    product = get_object_or_404(Product, pk=item_id)
    wishlist = get_object_or_404(Wishlist, user=request.user.id)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.info(request, 'Removed item from your wishlist')
    else:
        messages.error(request, 'That product is not in your wishlist!')
    if redirect_from == 'wishlist':
        redirect_url = reverse('view_wishlist')
    else:
        redirect_url = reverse('product_detail', args=[item_id])
    return redirect(redirect_url)


@login_required
def transfer_all_to_cart(request):
    ''' Add all items on the wishlist to the shopping cart.

    If the items are already in the cart it increments the quantity
    by 1. It then sets the cart in session equal to the cart object
    which contains the new quantities.

    Args:
        request (object): HTTP request object.
    Returns:
        Redirects view_cart page if successful.
        Redirects back to the wishlist page if unsuccessful.
    '''
    # If cart is in session, get it or else create one
    cart = request.session.get('cart', {})

    # try:
    wishlist = Wishlist.objects.filter(user=request.user.id)[0]

    # except IndexError:
    #     messages.error(request, "There's nothing to add!")
    #     return redirect(reverse('view_wishlist'))
    # else:
    wishlist_items = wishlist.products.all()

    if wishlist_items:
        for item in wishlist_items:
            product = get_object_or_404(Product, sku=item)
            quantity = 1
            if str(product.id) in list(cart.keys()):
                cart[str(product.id)] += quantity
            else:
                cart[str(product.id)] = quantity
        messages.success(request, 'Added all items to your cart')
        request.session['cart'] = cart
        return redirect(reverse('view_cart'))

    messages.error(request, "There's nothing to add!")
    return redirect(reverse('view_wishlist'))
