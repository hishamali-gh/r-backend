from rest_framework import serializers
from .models import CartItem, Cart
from products.serializers import ProductVariantModelSerializer
from products.models import ProductVariant


class CartItemModelSerializer(serializers.ModelSerializer):
    variant = ProductVariantModelSerializer(read_only=True)

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'variant', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.variant.final_price * obj.quantity


class CartModelSerializer(serializers.ModelSerializer):
    items = CartItemModelSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items']


class AddToCartModelSerializer(serializers.ModelSerializer):
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(),
        source='variant'
    )

    class Meta:
        model = CartItem
        fields = ['variant_id', 'quantity']

    def validate(self, data):
        variant = data['variant']
        quantity = data['quantity']

        if variant.stock < quantity:
            raise serializers.ValidationError(
                "Not enough stock available"
            )

        return data
