from django.core.mail import send_mail
from psycone.settings import EMAIL_FROM_SENDGRID
from django.utils.html import strip_tags
from django.http import HttpResponse

def send_email_task(subject, message, to_email):
    plain_message = strip_tags(message)
    try:
        send_mail(subject, plain_message, EMAIL_FROM_SENDGRID, to_email, html_message=message)
    except:
        return HttpResponse('Invalid header found.')
