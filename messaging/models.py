from django.db import models
from django.contrib.auth.models import User


class UserMessage(models.Model):
    """ A user or admin message relating to a reference number
    """
    ref_number = models.CharField(max_length=32)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    user_message = models.TextField()
    message_date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.user_message[:30]
