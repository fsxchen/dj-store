from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializer import SmsSerializer, UserRegisterSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from .models import VerifyCode

from random import choice

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户的验证
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username)| Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = "1234567890"
        random_string = []
        for i in range(4):
            random_string.append(choice(seeds))
        return "".join(random_string)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.data.get("mobile")
        code = self.generate_code()
        yunpian = YunPian('api_key', code, mobile)
        sms_status = self.perform_create(serializer)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin,
                  # mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    create:
        用户注册
    Re
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    permission_classes = (permissions.IsAuthenticated, )

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegisterSerializer
        return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = payload
        re_dict["name"] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)

        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_object(self):
        return self.request.user