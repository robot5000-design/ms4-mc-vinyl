import json
import time

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from mc_vinyl import settings

from products.models import Product
from profiles.models import UserProfile
from utils.helper_functions import send_confirmation_email
from .models import Order, OrderLineItem


class StripeWH_Handler:
    ''' Class to handle Stripe webhooks
    '''

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        ''' Handle a generic/unknown/unexpected webhook event

        Returns:
            HTTP Response object.
        '''
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        ''' Handle the payment_intent.succeeded webhook from Stripe

        If the order already exists in the database an email is sent to the
        customer and a succesful http response returned to stripe.
        If not the order is generated from the intent object contents and
        user profile and saved and an email is sent to the customer and
        a succesful http response returned to stripe. If there are any errors a
        http error response is returned to stripe.

        Returns:
            HTTP Response object.
        '''
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        cart_items = []
        product_count = 0
        for item_id, quantity in eval(cart).items():
            product = get_object_or_404(Product, pk=item_id)
            product_count += quantity
            cart_items.append({
                'quantity': quantity,
                'product': product,
            })

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_full_name = shipping_details.name
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                # iexact exact non-case-sensitive match
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            subject_context = {'order': order}
            body_context = {
                    'order': order,
                    'cart_items': cart_items,
                    'contact_email': settings.DEFAULT_FROM_EMAIL
                }
            path = 'checkout/confirmation_emails/'
            send_confirmation_email(order.email, subject_context,
                                    body_context, path)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)

        order = None
        try:
            order = Order.objects.create(
                full_name=shipping_details.name,
                user_profile=profile,
                email=billing_details.email,
                phone_number=shipping_details.phone,
                country=shipping_details.address.country,
                postcode=shipping_details.address.postal_code,
                town_or_city=shipping_details.address.city,
                street_address1=shipping_details.address.line1,
                street_address2=shipping_details.address.line2,
                county=shipping_details.address.state,
                original_cart=cart,
                stripe_pid=pid,
            )
            for item_id, quantity in json.loads(cart).items():
                product = Product.objects.get(id=item_id)
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                )
                order_line_item.save()
        except Exception as exception:
            if order:
                order.delete()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {exception}',
                status=500)
        subject_context = {'order': order}
        body_context = {
                'order': order,
                'cart_items': cart_items,
                'contact_email': settings.DEFAULT_FROM_EMAIL
            }
        path = 'checkout/confirmation_emails/'
        send_confirmation_email(order.email, subject_context,
                                body_context, path)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        ''' Handle the payment_intent.payment_failed webhook from Stripe

        Returns:
            HTTP Response object.
        '''
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
