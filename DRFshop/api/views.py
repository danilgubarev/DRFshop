from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(stock=0)
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.prefetch_related('orders')
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    max_price = products.aggregate(max_price=Max('price'))['max_price'] or 0

    serializer = ProductInfoSerializer({
        'products': products,
        'count': products.count(),
        'max_price': max_price
    })

    return Response(serializer.data)
