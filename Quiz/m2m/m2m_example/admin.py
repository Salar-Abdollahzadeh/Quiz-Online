from django.contrib import admin
from .models import Group, MemberShip


# Register your models here.

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(MemberShip)
class MemberShipAdmin(admin.ModelAdmin):
    pass
