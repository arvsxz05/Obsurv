from django.contrib import admin

from Profile.models import User_Profile

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['owner__username']

admin.site.register(User_Profile, UserProfileAdmin)