import django_filters
from .models import Goods

class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(name="shop_price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(name="shop_price", lookup_expr='lte')
    # 不加lookup，就精确匹配
    name = django_filters.CharFilter(name="name", lookup_expr='icontains')

    class Meta:
        model = Goods
        fields = ["price_min", "price_max", 'name']