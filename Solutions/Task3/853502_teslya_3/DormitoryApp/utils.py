from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
import logging


def send_email_to_user(request, user):
    logger = logging.getLogger('django')
    current_site = get_current_site(request)
    email_subject = 'Activate your account'

    message = render_to_string('verification_email.html', {
        'user': user,
        'current_site': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': default_token_generator.make_token(user),
        'time_send': timezone.now(),

    })
    to_email = user.email
    email = EmailMessage(subject=email_subject, body=message, to=[to_email])
    email.content_subtype = 'html'
    email.send()
    logger.info('Email send to {}'.format(user.username))


class Sender:
    def __init__(self, request):
        self.request = request

    def __call__(self, user):
        send_email_to_user(self.request, user)


def send_rent_email_to_user(mess):
    logger = logging.getLogger('django')
    email_subject = 'Ответ на ваше заявление на аренду'
    print(mess.name)
    message = render_to_string('rent_email.html', {
        'name': mess.name,
        'time_send': timezone.now(),
        'text': mess.text,
        'cost': mess.cost,
    })
    to_email = mess.email
    email = EmailMessage(subject=email_subject, body=message, to=[to_email])
    email.content_subtype = 'html'
    email.send()
    logger.info('Rent mail send to {}'.format(mess.name))
