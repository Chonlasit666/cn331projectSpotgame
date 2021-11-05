from django.contrib import admin

# Register your models here.
from .models import playList, roomInfo, played, songModel


class playListAdmin(admin.ModelAdmin):
    filter_horizontal = ('song_list',)


class roomInfoAdmin(admin.ModelAdmin):
    filter_horizontal = ('player',)


admin.site.register(playList, playListAdmin)
admin.site.register(roomInfo, roomInfoAdmin)
admin.site.register(played)
admin.site.register(songModel)
