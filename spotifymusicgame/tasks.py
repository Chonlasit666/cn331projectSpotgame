from celery import shared_task
from .models import roomInfo

@shared_task
def add():
    x = roomInfo.objects.get(id=1).max_player
    return x


