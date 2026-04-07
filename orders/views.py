from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError

from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from .serializers import OrderSerializer
from .models import Order, OrderItem
from cart.models import Cart


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found"}, status=400)

        cart_items = cart.items.select_related(
            'variant',
            'variant__product',
            'variant__size'
        )

        if not cart_items.exists():
            return Response({"detail": "Cart is empty"}, status=400)

        shipping_data = request.data.get("shipping_details", {})

        order = Order.objects.create(
            user=user,
            name=shipping_data.get("name"),
            address=shipping_data.get("address"),
            city=shipping_data.get("city"),
            postal_code=shipping_data.get("postalCode"),
            phone=shipping_data.get("phone"),
        )

        total_price = 0

        for item in cart_items:
            variant = item.variant

            if variant.stock < item.quantity:
                raise ValidationError(
                    f"Not enough stock for {variant.product.name} ({variant.size.value})"
                )

            price = variant.final_price

            OrderItem.objects.create(
                order=order,
                variant=variant,
                quantity=item.quantity,
                price=price,
            )

            variant.stock -= item.quantity
            variant.save()

            total_price += price * item.quantity

        order.total_price = total_price
        order.save()

        cart_items.delete()

        return Response({"detail": "Order created successfully"})


class AdminOrderAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.select_related('user').prefetch_related(
            'items__variant__product',
            'items__variant__size'
        )

        if self.request.user.is_staff:
            return queryset.order_by('-created_at')

        return queryset.filter(user=self.request.user).order_by('-created_at')


class MonthlyRevenueAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        successful_orders = (
            Order.objects.filter(status='DELIVERED')
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(revenue=Sum('total_price'))
            .order_by('month')
        )

        chart_data = [
            {
                "month": item['month'].strftime('%b %Y'),
                "revenue": float(item['revenue'] or 0)
            }
            for item in successful_orders
        ]

        return Response(chart_data)
