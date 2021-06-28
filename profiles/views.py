from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile, UserMessage, AdminMessage
from .forms import UserProfileForm, UserMessageForm, AdminMessageForm

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
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))
    user_messages = UserMessage.objects.filter(ref_number=order_number)
    admin_messages = AdminMessage.objects.filter(ref_number=order_number)

    user_message_form = UserMessageForm(initial={
        'ref_number': order.order_number
    })
    admin_message_form = AdminMessageForm(initial={
        'ref_number': order.order_number
    })

    template = 'profiles/past_order.html'
    context = {
        'order': order,
        'user_messages': user_messages,
        'admin_messages': admin_messages,
        'user_message_form': user_message_form,
        'admin_message_form': admin_message_form,
    }

    return render(request, template, context)


def add_user_message(request, order_number):
    if request.method == 'POST':
        user_message_body = request.POST['user_message']
        user_message_form = UserMessageForm({
            'user_message': user_message_body,
            'ref_number': order_number,
        })

        if user_message_form.is_valid():
            user_message_form.save()
            messages.info(request, 'Successfully added a message!')
            return redirect(reverse('order_history', args=[order_number]))
        else:
            messages.error(request, 'Failed to add message. Please ensure the \
                           form is valid.')
        return redirect(reverse('order_history', args=[order_number]))