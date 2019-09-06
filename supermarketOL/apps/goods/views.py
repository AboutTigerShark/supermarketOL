from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from goods.models import Goods, GoodsCategory, Banner, HotSearchWords
from .serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer, \
    HotWordsSerializer
from django_filters import rest_framework
from rest_framework import filters
from .filters import GoodsFilter


# 修改分页样式(优先级高于settings.py)
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

# 方法一
# class GoodsListView(APIView):
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods, many=True)
#         return Response(goods_serializer.data)


from rest_framework import mixins, viewsets
from rest_framework import generics

# 方法二
# class GoodsListView(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# 方法三
# ListCreateAPIView封装了get,post，原理同方法二
# class GoodsListView(generics.ListCreateAPIView):
#     queryset = Goods.objects.all()[:20]
#     serializer_class = GoodsSerializer
#     pagination_class = StandardResultsSetPagination


# 方法四
class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination
    # authentication_classes = (JSONWebTokenAuthentication,)
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['name', 'goods_brief', 'goods_desc']  # 搜索
    filter_class = GoodsFilter  # 过滤
    ordering_fields = ['sold_num', 'shop_price']  # 排序


# Retrieve能获取某个商品的详情,甚至url已经帮我们配好
class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    list:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer


