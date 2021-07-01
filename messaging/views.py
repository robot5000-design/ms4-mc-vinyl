from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserMessage
from .forms import UserMessageForm


@login_required
def messaging(request):
    """ Display messages
    """
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
    template = 'messaging/messaging.html'
    context = {
        'all_messages': all_messages,
    }

    return render(request, template, context)


@login_required
def view_message_thread(request, ref_number):
    """ Display a thread of messages
    """
    message_thread = (UserMessage.objects
                      .filter(ref_number=ref_number)
                      .order_by('-message_date')
                      )
    for message in message_thread:
        message.read = True
        message.save()
    user = message_thread[0].user
    message_form = UserMessageForm()
    template = 'messaging/message_thread.html'
    context = {
        'message_thread': message_thread,
        'ref_number': ref_number,
        'message_form': message_form,
        'user': user,
    }
    return render(request, template, context)


@login_required
def add_admin_reply(request, ref_number):
    """ Adds an admin message reply
    """
    if request.method == 'POST':
        message_form = UserMessageForm(request.POST)

        if message_form.is_valid():
            UserMessage.objects.create(
                ref_number=ref_number,
                user=request.user,
                user_message=request.POST['user_message'],
            )
            messages.info(request, 'Successfully added a message!')
            return redirect(reverse('view_message_thread', args=[ref_number]))
        else:
            messages.error(request, 'Failed to add message. Please ensure the \
                           form is valid.')
        return redirect(reverse('view_message_thread', args=[ref_number]))
