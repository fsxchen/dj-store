from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav
from .models import UserLeavingMessage, UserAddress
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


class LeavingMessageSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True)
    class Meta:
        model = UserLeavingMessage
        fields = ("id","user", "message_type", "subject", "message", "file", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserAddress
        fields = ( "id", "user", "province", "city", "district", "mobile")