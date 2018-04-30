from django.shortcuts import render

# Create your views here.

# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics

from .models import Goods
from .serializer import GoodsSerizlizer


# class GoodsListView(APIView):
#     """
#     商品列表
#     """
#     def get(self, response):
#         goods = Goods.objects.all()[:20]
#         goods_serializer = GoodsSerizlizer(goods, many=True)
#         return Response(goods_serializer.data)
#
#     def post(self, request):
#         serializer = GoodsSerizlizer(data=request.data)
#         if serializer.validated_data():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.pagination import PageNumberPagination

class StandarResultSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "p"
    max_page_size = 100

# class GoodsListView(generics.ListAPIView):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerizlizer
#     pagination_class = StandarResultSetPagination
#




# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerizlizer
#
#     def get(self, requset, *args, **kwargs):
#         return self.list(requset, *args, **kwargs)

from rest_framework import viewsets

class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerizlizer
    pagination_class = StandarResultSetPagination