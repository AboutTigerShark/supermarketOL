# import django_filters
from django.db.models import Q
from django_filters import rest_framework

from goods.models import Goods


class GoodsFilter(rest_framework.FilterSet):
    """
    商品的过滤类
    """
    pricemin = rest_framework.NumberFilter(field_name='shop_price', lookup_expr='gte')
    pricemax = rest_framework.NumberFilter(field_name='shop_price', lookup_expr='lte')
    top_category = rest_framework.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']
