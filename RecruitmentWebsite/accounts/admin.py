from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','bio', 'resume', 'user']

UserAdmin.list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(Profile, ProfileAdmin)
