# coding=utf-8
"""supermarketOL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

# from goods.views import GoodsListView
from supermarketOL.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, IndexCategoryViewset
from trade.views import ShoppingCartViewSet, OrderViewSet, AlipayView
from user_operations.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressViewset
from users.views import SmsCodeViewSet, UserViewSet

import xadmin

# 方法一
# goods_list = GoodsListViewSet.as_view(
#     {'get': 'list'},
# )
# urlpatterns = [

#
#     re_path(r'^goods/', goods_list, name='goods_list'),
# ]

router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, basename='goods')
router.register(r'categorys', CategoryViewSet, basename='categorys')
router.register(r'code', SmsCodeViewSet, basename='code')
router.register(r'users', UserViewSet, basename='users')
router.register(r'userfavs', UserFavViewSet, basename='userfavs')
router.register(r'leavingmessage', UserLeavingMessageViewSet, basename='leavingmessage')
router.register(r'useraddress', UserAddressViewset, basename='useraddress')
router.register(r'shopcarts', ShoppingCartViewSet, basename='shopcarts')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'banners', BannerViewSet, basename='banners')
router.register(r'indexgoods', IndexCategoryViewset, basename='indexgoods')

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'docs/', include_docs_urls(title='超市在线')),
    # re_path(r'^goods/', GoodsListView.as_view(), name='goods_list'),
    path('', include(router.urls)),
    re_path(r'^login/', obtain_jwt_token),
    re_path(r'^alipay/return/', AlipayView.as_view(), name="alipay"),

]
