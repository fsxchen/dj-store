from django.shortcuts import render
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Create your views here.

# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Goods, GoodsCategory, Banner
from .serializer import GoodsSerizlizer, GoodsCategorySerializer, BannerSerializer
from .serializer import IndexCategorySerializer
from .filters import ProductFilter

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
from rest_framework.authentication import TokenAuthentication


class GoodsListViewSet(CacheResponseMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerizlizer
    pagination_class = StandarResultSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = ProductFilter
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    search_fields = ('name', "goods_brief", "goods_desc")
    ordering_fields = ('sold_num', 'shop_price')
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        商品详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(is_tab=True)
    serializer_class = IndexCategorySerializer