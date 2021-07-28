import json
import stripe

from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
    )
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q

from cart.contexts import cart_contents
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from messaging.models import UserMessage
from .forms import OrderForm
from .models import Order, OrderLineItem


@require_POST
def cache_checkout_data(request):
    ''' Caches the checkout data to be used in the event of a failure or
    interuption of the normal flow of the stripe payment.

    Args:
        request (object): HTTP request object.
    Returns:
        A HTTP Response (to the JS post request).
    '''
    try:
        # get the payment intent id
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except IndexError as exception:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=exception, status=400)


def checkout(request):
    ''' Handles checkout with stripe and generates the stripe payment
    intent.

    Populates, validates and saves the order form. Checks that each product
    ordered actually exists in the database.

    Args:
        request (object): HTTP request object.
    Returns:
        Render of the checkout template.
        A redirect to a specific url if a post request.
    '''
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = request.POST['email']

        form_data = {
            'full_name': request.POST['full_name'],
            'email': email,
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
            for item_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database."
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            request.session['order_number'] = order.order_number
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        messages.error(request, 'There was an error with your form. \
            Please double check your information.')

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(
            request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

    current_cart = cart_contents(request)
    stripe_total = round(current_cart['grand_total'] * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    # Attempt to prefill the form with any info the user maintains in
    # their profile
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            order_form = OrderForm(initial={
                'full_name': profile.default_full_name,
                'email': request.user.email,
                'phone_number': profile.default_phone_number,
                'country': profile.default_country,
                'postcode': profile.default_postcode,
                'town_or_city': profile.default_town_or_city,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'county': profile.default_county,
            })
        except UserProfile.DoesNotExist:
            order_form = OrderForm()
    else:
        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)


def checkout_success(request, order_number):
    ''' Handle successful checkouts

    For logged-in users:
        Save user profile to the order. Save profile form if requested.
    Otherwise:
        Display message of order success.

    Remove the cart from the session.

    Args:
        request (object): HTTP request object.
        order_number (uuid): unique order reference number.
    Returns:
        Render of the checkout success template.
    Raises:
        django Http404 exception - If there's an order number mismatch
        or order number does not exist in session. This could happen if
        a user tries to access through the url.
    '''
    if 'order_number' not in request.session:
        raise Http404("Sorry that page has expired!")
    if request.session['order_number'] != order_number:
        raise Http404("Order Numbers do not match!")

    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Add the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_full_name': order.full_name,
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']
    if 'order_number' in request.session:
        del request.session['order_number']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)


@login_required
def view_all_orders(request):
    ''' Allows the admin to view all orders

    Gets all orders on the database ordered by date to send
    to the template.

    Args:
        request (object): HTTP request object.
    Returns:
        Render of the all_orders template.
        A redirect to a specific home url if not a superuser.
    '''
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    orders = Order.objects.all().order_by('-date')

    if request.GET:
        if 'search_users' in request.GET:
            query = request.GET['search_users']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('view_all_orders'))

            if query.lower() == 'no account':
                queries = Q(user_profile=None)
            else:
                queries = Q(user_profile__user__username__icontains=query)

            orders = orders.filter(queries)

    template = 'checkout/all_orders.html'
    context = {
        'orders': orders,
    }
    return render(request, template, context)


@login_required
def view_order_detail(request, order_number):
    ''' Display order detail

    Gets a specific order detail and all messages associated with that
    order to send to the template.

    Args:
        request (object): HTTP request object.
        order_number (uuid): unique order reference number.
    Returns:
        Render of the order_detail template.
        A redirect to a specific home url if not a superuser.
    '''
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    message_thread = (UserMessage.objects
                      .filter(ref_number=order_number)
                      .order_by('-message_date')
                      )
    order = get_object_or_404(Order, order_number=order_number)

    template = 'checkout/order_detail.html'
    context = {
        'message_thread': message_thread,
        'order': order,
    }
    return render(request, template, context)
