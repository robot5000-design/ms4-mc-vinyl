from django.shortcuts import (
    render, redirect, reverse,
    HttpResponse, get_object_or_404)
from django.contrib import messages

from products.models import Product


def view_cart(request):
    """ A view that renders the cart contents page
    """
    template = 'cart/cart.html'

    return render(request, template)


def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart
    """
    product = get_object_or_404(Product, pk=item_id)
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
        messages.success(request, f'Updated {product.title} quantity to {cart[item_id]}')
    else:
        cart[item_id] = quantity
        messages.success(request, f'Added {product.title} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """Adjust the quantity of the specified product to the specified amount
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
        messages.info(request, f'Updated {product.title} quantity to {cart[item_id]}')
    else:
        cart.pop(item_id)
        messages.info(request, f'Removed {product.title} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart
    """
    try:
        product = get_object_or_404(Product, pk=item_id)
        cart = request.session.get('cart', {})

        cart.pop(item_id)
        messages.info(request, f'Removed {product.title} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
