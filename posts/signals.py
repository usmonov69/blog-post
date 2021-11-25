from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Author
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def post_save_create_user_to_author(sender, created, instance, **kwargs):
	if created:
		Author.objects.create(user=instance) 