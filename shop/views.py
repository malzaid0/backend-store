from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from .models import Category, Product, Image, Order
from .serializers import ProductsListSerializer, RegisterSerializer, CartSerializer


class ProductsList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer


class Register(CreateAPIView):
    serializer_class = RegisterSerializer


class UserCart(RetrieveAPIView):
    queryset = Order.objects.filter(is_paid=False)
    lookup_field = "buyer_id"
    lookup_url_kwarg = "user_id"
    serializer_class = CartSerializer
