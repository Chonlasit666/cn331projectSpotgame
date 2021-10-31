from django.contrib import admin

# Register your models here.
from .models import playList,roomInfo,played,songModel

admin.site.register(playList)
admin.site.register(roomInfo)
admin.site.register(played)
admin.site.register(songModel)
