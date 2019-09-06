# coding=utf-8
import random
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status, permissions, authentication
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from .serializers import SsmSerializer, UserRegSerializer, UserDetailSerializer
from tools.yunpianyanzhengma.yunpian import YunPian
from .models import VerifyCode
from supermarketOL.settings import API_KEY


User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CustomBackend(ModelBackend):
    """
    自定义用户验证(登录时验证)
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SsmSerializer

    def generate_code(self):
        """
        随机生成四位数字验证码
        :return:
        """
        code = []
        for i in range(4):
            code.append(str(random.randint(0, 9)))
        return "".join(code)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']

        yun_pian = YunPian(API_KEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                'mobile': sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_save = VerifyCode(code=code, mobile=mobile)  # 发送成功将验证码保存到数据库
            code_save.save()
            return Response({
                'mobile': mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    用户
    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # request.data是一个QueryDict,与self.initial_data的数据相同
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        # 获得token和username
        user_dict = serializer.validated_data  # serializer.validated_data返回一个OrderedDict
        payload = jwt_payload_handler(user)
        user_dict['token'] = jwt_encode_handler(payload)
        user_dict['username'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(user_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    # 重载此方法，返回一个instance
    def perform_create(self, serializer):
        return serializer.save()


