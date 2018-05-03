from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import mixins

from .models import UserFav
from .serializer import UserFavSerializer


class UserFavViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
