from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email', 'sex')
    search_fields = ('name',)


admin.site.register(User,UserAdmin)