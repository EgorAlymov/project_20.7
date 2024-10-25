from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import article_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from gamestock.models import Response
from decouple import config


@receiver(article_save, sender=Response)
def send_mail(sender, instance, created, **kwargs):
    if created:
        user = instance.article.author

        html = render_to_string(
            'board/messages/new_response.html',
            {
                'user': user,
                'response': instance,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'New response',
            from_email=config('EMAIL_HOST_USER'),
            to=[user.email]
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()
    else:
        user = instance.author

        html = render_to_string(
            'board/messages/update_response.html',
            {
                'user': user,
                'comment': instance,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'Your response received',
            from_email=config('EMAIL_HOST_USER'),
            to=[user.email]
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()