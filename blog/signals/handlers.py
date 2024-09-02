from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from blog.models import Publisher

User = get_user_model()


@receiver(post_save, sender=User)
def create_publisher_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        Publisher.objects.create(user=kwargs["instance"])
