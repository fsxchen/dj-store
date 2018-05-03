import django_filters
from .models import Goods
from django.db.models import Q

class ProductFilter(django_filters.FilterSet):
    pricemin = django_filters.NumberFilter(name="shop_price", lookup_expr="gte")
    pricemax = django_filters.NumberFilter(name="shop_price", lookup_expr='lte')
    # 不加lookup，就精确匹配
    name = django_filters.CharFilter(name="name", lookup_expr='icontains')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))


    class Meta:
        model = Goods
        fields = ["pricemin", "pricemax", 'name', 'is_hot']