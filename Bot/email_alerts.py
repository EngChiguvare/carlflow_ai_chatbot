from django.core.mail import send_mail
from django.conf import settings


def send_hot_lead(phone, message):
    send_mail(
        subject='🔥 HOT Lead - Carlflow_AI',
        message=f'Phone: {phone}\n\nMessage:\n{message}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False
    )