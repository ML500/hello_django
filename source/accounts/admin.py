from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import AuthToken, Profile
from django.contrib.auth.admin import UserAdmin

admin.site.register(AuthToken)


class ProfileInline(admin.StackedInline):
    model = Profile
    exclude = []


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


User = get_user_model()
admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
