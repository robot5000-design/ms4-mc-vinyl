from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from utils.helper_functions import send_confirmation_email
from mc_vinyl import settings
from messaging.forms import UserMessageForm
from messaging.models import UserMessage
from checkout.models import Order
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    ''' Display and edit the user's profile. Display order summary.

    Args:
        request (object): HTTP request object.
    Returns:
        Render of the profile template.
        Redirects to the profile page after update or failed update.
    '''
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request,
                           'Update failed. Please ensure the form is valid.')
        return redirect(reverse('profile'))

    form = UserProfileForm(instance=user_profile)
    orders = user_profile.orders.all().order_by('-date')

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
        'user_profile': user_profile,
    }
    return render(request, template, context)


@login_required
def order_history(request, order_number):
    ''' Display the history including messages of a past order.

    Gets past details on an order and all associated messages.
    Renders a user message form so that the user can send a message regarding
    the order.

    Args:
        request (object): HTTP request object.
        order_number (uuid): unique order reference number.
    Returns:
        Render of the past_order template.
    '''
    order = get_object_or_404(Order, order_number=order_number)

    if request.user != order.user_profile.user:
        messages.error(request, 'Order does not match user!')
        return redirect(reverse('home'))

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))
    message_thread = (UserMessage.objects
                      .filter(ref_number=order_number)
                      .order_by('-message_date')
                      )
    message_form = UserMessageForm()

    template = 'profiles/past_order.html'
    context = {
        'order': order,
        'message_thread': message_thread,
        'message_form': message_form,
    }
    return render(request, template, context)


@login_required
def add_user_message(request, order_number):
    ''' Handles the sending of a user message regarding a past order.

    If the user message form is valid the message is saved and an email is
    sent to the admin.

    Args:
        request (object): HTTP request object.
        order_number (uuid): unique order reference number.
    Returns:
        Redirects to the same order history page.
    '''
    if request.method == 'POST':
        message_form = UserMessageForm(request.POST)

        if message_form.is_valid():
            UserMessage.objects.create(
                ref_number=order_number,
                user=request.user,
                user_message=request.POST['user_message'],
            )
            messages.info(request, 'Successfully added a message!')

            message = request.POST['user_message']
            send_email_address = settings.EMAIL_HOST_USER
            subject_context = {'ref_number': order_number}
            body_context = {
                    'user': request.user,
                    'ref_number': order_number,
                    'message': message,
                }
            path = 'profiles/confirmation_emails/'
            send_confirmation_email(send_email_address, subject_context,
                                    body_context, path)
        else:
            messages.error(request, 'Failed to add message. Please ensure the \
                           form is valid.')

    return redirect(reverse('order_history', args=[order_number]))
