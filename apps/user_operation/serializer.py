from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav
from goods.serializer import GoodsSerizlizer

class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerizlizer()
    class Meta:
        model = UserFav
        fields = ( 'goods', 'id')

class UserFavSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserFav
        fields = ('user', 'goods', 'id')
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),   # 在model中设置了，这里可以不设置。
                message="已经收藏"            # 可以作用在字段上，但是这里有两个
                                            # 字段
            )
        ]
