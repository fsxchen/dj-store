from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .models import UserFav
from .serializer import UserFavSerializer, UserFavDetailSerializer
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

