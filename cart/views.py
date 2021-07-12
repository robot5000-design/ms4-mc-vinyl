from django.shortcuts import (
    render, redirect, reverse,
    HttpResponse, get_object_or_404)
from django.contrib import messages

from products.models import Product


def view_cart(request):
    """ A view that renders the cart contents page

    Args:
        request (object): HTTP request object.
    Returns:
        Render of a template.
    """
    template = 'cart/cart.html'

    return render(request, template)


def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart

    Args:
        request (object): HTTP request object.
        item_id (int): numerical id which identifies a product
    Returns:
        A redirect to a specific url.
    """
    if request.POST.get('quantity'):
        quantity = int(request.POST.get('quantity'))
    else:
        quantity = 1
    if request.POST.get('redirect_url'):
        redirect_url = request.POST.get('redirect_url')
    else:
        redirect_url = reverse('view_cart')
    # If cart is in session, get it or else create one
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
        messages.success(request, f'Updated item quantity to {cart[item_id]}')
    else:
        cart[item_id] = quantity
        messages.success(request, 'Added item to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """Adjust the quantity of the specified product to the specified amount.

    Args:
        request (object): HTTP request object.
        item_id (int): numerical id which identifies a product
    Returns:
        A redirect to a specific url.
    """
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
        messages.info(request, f'Updated item quantity to {cart[item_id]}')
    else:
        try:
            cart.pop(item_id)
            messages.info(request, 'Removed item from your cart')
        except KeyError as e:
            messages.error(request, f'Error removing item: {e}')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart

    Args:
        request (object): HTTP request object.
        item_id (int): numerical id which identifies a product
    Returns:
        A redirect to a specific url.
    """
    cart = request.session.get('cart', {})
    try:
        cart.pop(item_id)
        messages.info(request, 'Removed item from your cart')

        request.session['cart'] = cart
        return redirect(reverse('view_cart'))

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return redirect(reverse('view_cart'))
