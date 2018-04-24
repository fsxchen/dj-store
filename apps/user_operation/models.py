from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

User = get_user_model()


# Create your models here.
class UserFav(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    goods = models.ForeignKey(Goods)
    add_time = models.DateTimeField(datetime.now, verbose_name="添加的时间")

    class Meta:
        verbose_name = "收藏的商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name