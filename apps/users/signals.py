
from django.db.models import signals
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from myproject import settings
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        # instance.set_password(password)
        # 重载 create 也可实现密码的加密。
        instance.save()
        # Token