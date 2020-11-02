from rest_framework.generics import ListAPIView
from .models import Category, Product, Image
from .serializers import ProductsListSerializer


class ProductsList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer
