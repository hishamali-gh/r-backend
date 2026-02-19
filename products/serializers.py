from rest_framework import serializers
from .models import ProductType, ProductImage, Product

class ProductTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name']

class ProductImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'url']

class ProductModelSerializer(serializers.ModelSerializer):
    images = ProductImageModelSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'product_type',
            'description',
            'price',
            'count',
            'images',
            'is_active',
            'created_at',
            'updated_at'
        ]
