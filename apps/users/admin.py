from django.contrib import admin

# Register your models here.
from .models import UserProfile, VerifyCode

admin.site.register(UserProfile)
admin.site.register(VerifyCode)