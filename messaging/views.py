from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from utils.helper_functions import send_confirmation_email

from checkout.models import Order
from .models import UserMessage
from .forms import UserMessageForm


@login_required
def messaging(request):
    """ Display all messages.

    Gets all messages grouped by order reference number by getting
    distinct id's first and then using the id's to filter messages.
    Then presented to the template as either open or closed threads.

    Args:
        request (object): HTTP request object.
    Returns:
        Render of the messaging template.
        Redirects to home url if not superuser.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    open_threads = []
    closed_threads = []

    # help with the following code found here
    # https://stackoverflow.com/questions/30084107/django-query-with-order-by-distinct-and-limit-on-postgresql/32760239#32760239
    distinct_ids = (UserMessage.objects
                    .order_by('ref_number', '-message_date')
                    .distinct('ref_number')
                    .values('id')
                    )
    all_messages = (UserMessage.objects
                    .filter(id__in=distinct_ids)
                    .order_by('-message_date')
                    )
    for message in all_messages:
        if message.closed is False:
            open_threads.append(message)
        else:
            closed_threads.append(message)

    template = 'messaging/messaging.html'
    context = {
        'open_threads': open_threads,
        'closed_threads': closed_threads,
    }
    return render(request, template, context)


@login_required
def view_message_thread(request, ref_number):
    """ Display a thread of messages.

    Gets a thread of messages all associated with one order
    reference number. Gets the order, the associated user
    and a user message form and sends all this to the template.

    Args:
        request (object): HTTP request object.
        ref_number (uuid): unique order reference number.
    Returns:
        Render of the message_thread template.
        Redirects to home url if not superuser.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    message_thread = (UserMessage.objects
                      .filter(ref_number=ref_number)
                      .order_by('-message_date')
                      )
    message_thread.update(read=True)
    order = get_object_or_404(Order, order_number=ref_number)

    user = list(message_thread)[-1].user
    thread_status = message_thread[0].closed
    message_form = UserMessageForm()

    template = 'messaging/message_thread.html'
    context = {
        'message_thread': message_thread,
        'ref_number': ref_number,
        'message_form': message_form,
        'user': user,
        'thread_status': thread_status,
        'order': order,
    }
    return render(request, template, context)


@login_required
def add_admin_reply(request, ref_number):
    """ Adds an admin message reply.

    Facilitates the admin user to write a message response to a customer
    regarding a specific order.

    Args:
        request (object): HTTP request object.
        ref_number (uuid): unique order reference number.
    Returns:
        Render of the message_thread template.
        Redirects to home url if not superuser.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        message_form = UserMessageForm(request.POST)

        if message_form.is_valid():
            UserMessage.objects.create(
                ref_number=ref_number,
                user=request.user,
                user_message=request.POST['user_message'],
            )
            messages.info(request, 'Successfully added a message!')

            # send an email to customer
            order = get_object_or_404(Order, order_number=ref_number)
            customer_email = order.email
            subject_context = {'ref_number': ref_number}
            body_context = {
                    'user': request.user,
                    'ref_number': ref_number,
                }
            path = 'messaging/confirmation_emails/'
            send_confirmation_email(customer_email, subject_context,
                                    body_context, path)

            return redirect(reverse('view_message_thread', args=[ref_number]))

        messages.error(request, 'Failed to add message. Please ensure the \
                       form is valid.')
        return redirect(reverse('view_message_thread', args=[ref_number]))


@login_required
def delete_thread(request, ref_number):
    """ Removes all messages in a thread associated with a specific
    ref number.

    Args:
        request (object): HTTP request object.
        ref_number (uuid): unique order reference number.
    Returns:
        Render of the messaging template.
        Redirects to home url if not superuser.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        UserMessage.objects.filter(ref_number=ref_number).delete()
        messages.info(request, 'Message Thread Deleted.')
    else:
        messages.error(request, 'Invalid Method.')
    return redirect(reverse('messaging'))


@login_required
def change_thread_status(request, ref_number):
    """ Close/open a thread associated with a specific
    ref number.

    Args:
        request (object): HTTP request object.
        ref_number (uuid): unique order reference number.
    Returns:
        Render of the message_thread template.
        Redirects to home url if not superuser.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        message_thread = UserMessage.objects.filter(
            ref_number=ref_number).order_by('-message_date')
        try:
            if message_thread[0].closed is False:
                UserMessage.objects.filter(
                    ref_number=ref_number).update(closed=True)
            else:
                UserMessage.objects.filter(
                    ref_number=ref_number).update(closed=False)
        except IndexError as exception:
            messages.error(request, f'{exception}')
            return redirect(reverse('home'))
    else:
        messages.error(request, 'Invalid Method.')

    return redirect(reverse('view_message_thread', args=[ref_number]))
