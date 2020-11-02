from rest_framework import serializers
from .models import Category, Product, Image


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "img"]


class ProductsListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "price", "inventory", "date_added", "description", "category", "images"]

    def get_images(self, obj):
        images = Image.objects.filter(product=obj)
        return ImageSerializer(images, many=True).data
