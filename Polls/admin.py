from django.contrib import admin

# Register your models here.
from Polls.models import Survey_Questions, Survey_Choices, Responses, User_Profile

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['owner__username']

admin.site.register(Survey_Questions)
admin.site.register(Survey_Choices)
admin.site.register(Responses)
admin.site.register(User_Profile, UserProfileAdmin)