from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import playList, songModel



@receiver(post_save, sender=playList)
def create_track(sender, instance, created, **kwargs):
    if created:
        instance.create_track()

