from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializer import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    """
    list:
        获取用户收藏列表
    create：
        收藏商品
    """
    # queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

class LeavingMessageViewSet(mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收获
    create:
        创建
    """

    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
