import time

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from utils.permissions import IsOwnerOrReadOnly
# Create your views here.
from rest_framework import viewsets, mixins

from .models import OrderInfo

from .serializers import ShopCartSserializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderGoods



class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车功能详情
    list:
        获取购物车详情
    create:
        加入购物车

    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSserializer
    lookup_field = "goods"

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSserializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return  OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        else:
            return  OrderSerializer

    def generate_order_sn(self):
        from random import Random
        random_ins = Random()
        # 当前时间 + user id + 随机数
        order_sn = "{time_str}{userid}{randstr}".format(
            time_str=time.strftime("&Y%m%d%H%M%S",
                                   userid=self.request.user.id,
                                   randstr=random_ins.randint(10, 99))
        )
        return order_sn

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order

from rest_framework.views import APIView
from utils.alipay import AliPay
from myproject.settings import ali_pub_key_path, privat_key_path

class AliPayViewSet(APIView):
    def get(self,request):
        """
        处理支付宝return_url
        :param request:
        :return:
        """
        pass

    def post(self, request):
        """
        处理nofify消息,异步请求
        :param request:
        :return:
        """
        from datetime import datetime
        from rest_framework.response import Response
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value
        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016091500513709",
            app_notify_url="http://localhost:8001/alipay/return/",
            app_private_key_path=privat_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.92.87.172:8000/"
        )


        verify_re = alipay.verify(processed_dict, sign)
        if verify_re:
            order_sn = processed_dict["out_order_no"]
            trade_no = processed_dict.get("trade_no", None)
            trade_status = processed_dict.get("trade_status", None)
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            from django.shortcuts import redirect
            response = redirect("index")
            response.set_cookie("nexPath", "pay", max_age=2)
            return response
        else:
            response = redirect("index")
            return response
