from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户的验证
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username)| Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None