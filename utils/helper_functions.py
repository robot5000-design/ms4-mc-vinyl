from django.template.loader import render_to_string
from django.core.mail import send_mail
from mc_vinyl import settings


def send_confirmation_email(email_address, subject_context,
                            body_context, path):
    ''' Send the user a confirmation email

    Args:
        email_address (str): Email address to send email to.
        subject_context (str): Subject context of the email.
        body_context (str): Body context of the email.
        path (str): Path to email text files.
    '''
    send_to_email = email_address
    subject = render_to_string(
        f'{path}email_subject.txt',
        subject_context
    )
    body = render_to_string(
        f'{path}email_body.txt',
        body_context
    )
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [send_to_email]
    )
