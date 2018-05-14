from django.db.models.signals import post_save, post_delete
from django.db.models import signals
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from myproject import settings
from django.contrib.auth import get_user_model

from  user_operation.models import UserFav

User = get_user_model()

@receiver(post_save, sender=User)
def creater_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=User)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
