from django.contrib import admin
from .models import Profile, Past_Education_Details, Current_Education_Details, Other_Details
# Register your models here.
admin.site.register(Profile)
admin.site.register(Past_Education_Details)
admin.site.register(Current_Education_Details)
admin.site.register(Other_Details)