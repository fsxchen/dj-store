from django.contrib import admin
from .models import UserFav
from .models import UserAddress
from .models import UserLeavingMessage
# Register your models here.

admin.site.register(UserLeavingMessage)
admin.site.register(UserFav)
admin.site.register(UserAddress)
