from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(playList)
admin.site.register(roomInfo)
admin.site.register(played)
admin.site.register(songModel)

