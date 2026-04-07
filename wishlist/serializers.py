from rest_framework import serializers
from products.serializers import ProductModelSerializer
from .models import Wishlist
from products.models import Product


class WishlistModelSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    product = ProductModelSerializer(read_only=True)

    has_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_id', 'has_stock', 'created_at']
        read_only_fields = ['id', 'created_at']
