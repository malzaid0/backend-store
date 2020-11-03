from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Category, Product, Image
from .serializers import ProductsListSerializer, RegisterSerializer


class ProductsList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer


class Register(CreateAPIView):
    serializer_class = RegisterSerializer
