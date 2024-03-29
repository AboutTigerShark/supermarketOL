# coding=utf-8
from datetime import datetime, timedelta
import re

from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from users.models import VerifyCode

User = get_user_model()

REGEX_MOBILE = r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$'  # 手机号正则匹配


class SsmSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)


    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """

        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')

        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码不合法')

        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile):
            raise serializers.ValidationError('距上一次发送不足一分钟')

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    # UniqueValidator用于判断字段唯一性
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    # style={'input_type': 'password'},在模板的input标签中设定type='password'
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    # 重载create使得在User在保存时将密码设置为密文
    # def create(self, validated_data):
    #
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        # self.initial_data是一个QueryDict，存着表单post过来的数据
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    # code是多余字段，验证完就删除
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ["username", "code", "mobile", "password"]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "gender", "birthday", "email", "mobile"]
