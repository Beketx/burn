import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from developer.models import Developer, DeveloperService, Favorites
from userauth.models import User

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Developer)
def developer_created(sender, instance, created, **kwargs):
    if created:
        logger.debug("Developer created")

@receiver(post_delete, sender=Favorites)
def favorite_bool(sender, instance, **kwargs):
    if instance.favorite_bool == False:
        Favorites.objects.get(developer=instance.developer).delete()
