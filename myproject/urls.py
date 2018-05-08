"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from myproject.settings import MEDIA_ROOT
from django.views.static import serve
# from goods.views import GoodsListView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from users.views import SmsCodeViewSet

from goods.views import GoodsListViewSet, CategoryViewSet
from users.views import UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet

from trade.views import ShoppingCartViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'goods', GoodsListViewSet)
router.register(r'categorys', CategoryViewSet, base_name="categorys")
router.register(r'code', SmsCodeViewSet, base_name="codeview")
router.register(r'users', UserViewSet, base_name="user")
router.register(r'user_fav', UserFavViewSet, base_name="user_fav")
router.register(r'message', LeavingMessageViewSet, base_name="message")
router.register(r'address', AddressViewSet, base_name="address")
router.register(r'shopping', ShoppingCartViewSet, base_name="shopping")
router.register(r'orders', OrderViewSet, base_name="orders")

# from goods.views import GoodsListViewSet

goods_list = GoodsListViewSet.as_view({
    "get": 'list',
})

from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from trade.views import AliPayViewSet
from django.views.generic import TemplateView

urlpatterns = [
    url(r'index', TemplateView.as_view(template_name="index")),
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-token-auth/', views.obtain_auth_token),
    # 商品列表页
    # url(r'goods/$',goods_list, name="goods-list"),
    url(r'^', include(router.urls)),
    url(r'^login/', obtain_jwt_token),
    url(r'docs/', include_docs_urls(title="文档")),
    url(r'^alipay/return/', AliPayViewSet.as_view(), name="alipay")
]
