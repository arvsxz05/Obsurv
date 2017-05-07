from django.contrib import admin

# Register your models here.
from Polls.models import Survey_Questions, Survey_Choices, Responses

admin.site.register(Survey_Questions)
admin.site.register(Survey_Choices)
admin.site.register(Responses)