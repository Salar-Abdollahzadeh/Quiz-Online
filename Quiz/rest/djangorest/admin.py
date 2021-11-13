from django.contrib import admin

from .models import Album, Track, Singer


# Register your models here.


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass


@admin.register(Singer)
class Singer(admin.ModelAdmin):
    pass