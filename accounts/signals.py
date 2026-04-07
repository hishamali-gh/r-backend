from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **args):
    if created and instance.email:
        send_mail(
            subject='Welcome to Willow',
            message=f"Hi, {instance.username}, welcome to Willow!",
            from_email=None,
            recipient_list=[instance.email],
            fail_silently=False
        )
