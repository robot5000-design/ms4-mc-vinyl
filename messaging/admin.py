from django.contrib import admin
from .models import UserMessage


class UserMessageAdmin(admin.ModelAdmin):
    list_display = (
        'ref_number',
        'user_message',
        'message_date',
    )


admin.site.register(UserMessage, UserMessageAdmin)
