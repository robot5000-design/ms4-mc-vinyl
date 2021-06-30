from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import UserMessage


@login_required
def messaging(request):
    """ Display messages
    """
    all_messages = UserMessage.objects.all()

    template = 'messaging/messaging.html'
    context = {
        'all_messages': all_messages,
    }

    return render(request, template, context)


@login_required
def view_message_thread(request, ref_number):
    """ Display a thread of messages
    """
    message_thread = UserMessage.objects.filter(ref_number=ref_number)
    for message in message_thread:
        message.read = True
        message.save()
    template = 'messaging/message_thread.html'
    context = {
        'message_thread': message_thread,
    }

    return render(request, template, context)
