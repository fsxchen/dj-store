from django.db import models
# from users.models import UserProfile
# Create your models here.
from django.contrib.auth import get_user_model
from goods.models import Goods

from datetime import datetime

User = get_user_model()


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    nums = models.IntegerField()
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return self.user.goods.name


class OrderInfo(models.Model):

    PAY_STATUS = (
        ("TRADE_SUCESS", "支付成功"),
        ("TRADE_CLOSED", "超市关闭"),
        ("WAIT_BUYER_PAY", "待支付"),
        ("TRADE_FINISHED", "交易已完成，不可退款")
    )

    PAY_TYPE = (
        ("alipay", "支付宝"),
        ("wechat", "微信")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=11, unique=True, verbose_name="订单编号", null=True)
    trade_no = models.CharField(max_length=13, unique=True, verbose_name="交易编号", blank=True)
    pay_status = models.CharField(max_length=10, choices=PAY_STATUS, verbose_name="订单状态")
    post_script = models.CharField(max_length=200, verbose_name="订单留言")
    order_mount = models.FloatField(max_length=11, default=0.0, verbose_name="订单金额")
    pay_time = models.DateTimeField(verbose_name="支付时间", default=datetime.now)

    address = models.CharField(max_length=100, default="", verbose_name="收货地址")
    signer_name = models.CharField(max_length=20, default="", verbose_name="签收人")
    singer_mobile = models.CharField(max_length=11, verbose_name="联系电话")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name


class OrderGoods(models.Model):
    """
    订单的商品详情
    """
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, related_name="goods")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单的商品详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.order_sn

