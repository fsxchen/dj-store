from datetime import datetime
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
class UserProfile(AbstractUser):
    """
    UserProfile
    """
    name = models.CharField(max_length=10, verbose_name="名字")
    birthday = models.DateField("出生日期", null=True, blank=True, verbose_name="出生年月")
    mobile = models.CharField(max_length=11)
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female")
    email = models.CharField(max_length=100, null=True, verbose_name="邮箱")


    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.name

class VerifyCode(models.Model):
    """
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
