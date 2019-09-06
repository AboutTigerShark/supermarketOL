from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.
from user_operations.models import UserFav, UserLeavingMessage, UserAddress
from user_operations.serializers import UserFavSerializer, UserLeavingMessageSerializer, UserAddressSerializer, \
    UserFavDetailSerializer
from util.permissions import IsOwnerOrReadOnly


class UserFavViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin):
    """
      list:
          获取用户收藏列表
      retrieve:
          判断某个商品是否已经收藏
      create:
          收藏商品
      """
    serializer_class = UserFavSerializer
    # lookup_field字段用于url查询
    lookup_field = "goods_id"
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

        # def perform_create(self, serializer):
        #     instance = serializer.save()
        #     goods = instance.goods
        #     goods.fav_num += 1
        #     goods.save()

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer


class UserLeavingMessageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                                mixins.DestroyModelMixin):
    """
     list:
         获取用户留言
     create:
         添加留言
     delete:
         删除留言功能
     """
    # queryset = UserLeavingMessage.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserLeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewset(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
