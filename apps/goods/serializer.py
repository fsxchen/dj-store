
from rest_framework import serializers
from .models import Goods, GoodsCategoryBrand
from .models import GoodsCategory
from .models import GoodsImage, Banner, IndexAd
# class GoodsSerizlizer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()
#
#     def create(self, validated_data):
#
#         return Goods.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerizlizer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'

    # def create(self, validated_data):
    #
    #     # return Goods.obj

class GoodsCategorySerializer3(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsCategorySerializer2(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    sub_cat = GoodsCategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsCategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    """
    商品类别序列化
    """

    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = GoodsCategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_ins = ad_goods[0].goods
            # 如果是嵌套serialization，image这种字段没法加入域名
            goods_json = GoodsSerizlizer(good_ins, many=False, context={"request": self.context["request"]}).data
        return goods_json


    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerizlizer(all_goods, many=True)
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"