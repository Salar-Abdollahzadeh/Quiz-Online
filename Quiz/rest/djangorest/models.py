from django.db import models


# Create your models here.


class Album(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=200)
    album = models.ForeignKey('Album', null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    singers = models.ManyToManyField('Singer')

    def __str__(self):
        if self.album:
            return f'{self.album.name} - {self.name}'
        return f'without_album - {self.name}'


class Singer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'
