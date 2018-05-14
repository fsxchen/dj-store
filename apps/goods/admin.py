from django.contrib import admin

# Register your models here.
from .models import Goods, GoodsCategory, GoodsImage
from .models import Banner, GoodsCategoryBrand, IndexAd

admin.site.register(Goods)
admin.site.register(GoodsCategory)
admin.site.register(Banner)
admin.site.register(GoodsCategoryBrand)
admin.site.register(GoodsImage)
admin.site.register(IndexAd)