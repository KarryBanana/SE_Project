from django.contrib import admin
from .models import Group, GroupPost, MemberShip

admin.site.register(Group)
admin.site.register(GroupPost)
admin.site.register(MemberShip)
