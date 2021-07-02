from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from utils.helper_functions import send_confirmation_email
from mc_vinyl import settings
from .models import UserProfile
from .forms import UserProfileForm
from messaging.forms import UserMessageForm
from messaging.models import UserMessage

from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request,
                           'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all().order_by('-date')

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }
    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))
    user_messages = UserMessage.objects.filter(ref_number=order_number)

    message_form = UserMessageForm()

    template = 'profiles/past_order.html'
    context = {
        'order': order,
        'user_messages': user_messages,
        'message_form': message_form,
    }
    return render(request, template, context)


def add_user_message(request, order_number):
    if request.method == 'POST':
        message_form = UserMessageForm(request.POST)

        if message_form.is_valid():
            UserMessage.objects.create(
                ref_number=order_number,
                user=request.user,
                user_message=request.POST['user_message'],
            )
            messages.info(request, 'Successfully added a message!')

            customer_email = settings.DEFAULT_FROM_EMAIL
            subject_context = {'ref_number': order_number}
            body_context = {
                    'user': request.user,
                    'ref_number': order_number,
                    'message': request.POST['user_message']
                }
            path = 'profiles/confirmation_emails/'
            send_confirmation_email(customer_email, subject_context,
                                    body_context, path)
            return redirect(reverse('order_history', args=[order_number]))
        else:
            messages.error(request, 'Failed to add message. Please ensure the \
                           form is valid.')
        return redirect(reverse('order_history', args=[order_number]))
