import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from rest_framework.validators import UniqueValidator
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    商品类别序列化
    """

    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否存在
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 手机是否合法

        # if re.match(REGEX_MOBILD, mobile):
        #     raise serializers.ValidationError("手机号码不合法")

        # 验证发送的频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile):
            raise serializers.ValidationError("距离上次操作不超过60s")

    class Meta:
        model = VerifyCode


class UserRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4,
                                 write_only=True,
                                 label="验证码",
                                 error_messages= {
                                     "required": "必填",
                                     "max_length": "4个字符"
                                 })
    username = serializers.CharField(required=True, allow_blank=True,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(required=True,
                                     write_only=True,
                                     style= {"input_type": "password"}
                                     )
    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


    def validate_code(self, code):
        verify_code = VerifyCode.objects.filter(
            code=code, mobile=self.initial_data["username"]).order_by("-add_time")
        # 使用initial可以获取输入中的数据
        if verify_code:
            last_recodrd = verify_code[0]
            now = datetime.now()
            import pytz
            now = now.replace(tzinfo=pytz.timezone('UTC'))
            five_minutes_ago = now - timedelta(hours=0, minutes=5,seconds=0)
            if five_minutes_ago > last_recodrd.add_time:
                raise serializers.ValidationError("验证码过期")
            if len(code) != 4:
                raise serializers.ValidationError("验证码错误！")
        else:
            raise serializers.ValidationError("验证码不存在")
        return code   # 不需要code，所以可以不用return

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")