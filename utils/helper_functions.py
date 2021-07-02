from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


def send_confirmation_email(email_address, subject, body):
    """Send the user a confirmation email"""
    email_address = email_address
    subject = render_to_string(subject)
    body = render_to_string(body)
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [email_address]
    )
