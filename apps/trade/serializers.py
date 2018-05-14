from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializer import GoodsSerizlizer
from utils.alipay import AliPay
from myproject.settings import ali_pub_key_path, privat_key_path

class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerizlizer(many=False)
    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCartSserializer(serializers.Serializer):

    user = serializers.HiddenField(
        default= serializers.CurrentUserDefault()
    )

    nums = serializers.IntegerField(required=True, min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能为1"
                                    })
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True)

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        instance.nums += validated_data["nums"]
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerizlizer(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):

    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        """
        生产支付的链接
        :param obj:
        :return:
        """
        alipay = AliPay(
            appid="2016091500513709",
            app_notify_url="http://localhost:8001/alipay/return/",
            app_private_key_path=privat_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.92.87.172:8000/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_no,
            total_amount=obj.total_amount,
            return_url="http://localhost:8001"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = '__all__'

    def generate_order_sn(self):
        from random import Random
        import time
        random_ins = Random()
        # 当前时间 + user id + 随机数
        order_sn = "{time_str}{userid}{randstr}".format(
                                    time_str=time.strftime("&Y%m%d%H%M%S"),
                                   userid=self.context["request"].user.id,
                                   randstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs