
from rest_framework import serializers
from .models import Goods
from .models import GoodsCategory
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



class GoodsSerizlizer(serializers.ModelSerializer):
    category = CategorySerializer()
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