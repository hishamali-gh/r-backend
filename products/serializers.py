from rest_framework import serializers
from .models import ProductType, ProductImage, Product, ProductVariant

class ProductTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name']

class ProductImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'url', 'main']
        read_only_fields = ['product']

class ProductModelSerializer(serializers.ModelSerializer):
    product_type = serializers.CharField(source='product_type.name', read_only=True)
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
            'images',
            'is_active',
            'created_at',
            'updated_at'
        ]

class ProductVariantModelSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'product_id', 'size', 'stock']
