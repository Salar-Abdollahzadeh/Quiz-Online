from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=200)


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField('Person', through='MemberShip')


class MemberShip(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=200)

