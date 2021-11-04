from django.contrib import admin

# Register your models here.
from .models import playList,roomInfo,played

admin.site.register(playList)
admin.site.register(roomInfo)
admin.site.register(played)
