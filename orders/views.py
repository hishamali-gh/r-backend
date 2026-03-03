from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework.generics import ListAPIView
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

        cart_items = cart.items.all()

        total_price = 0

        shipping_data = request.data.get("shipping_details", {})

        order = Order.objects.create(
            user=user,
            name=shipping_data.get("name"),
            address=shipping_data.get("address"),
            city=shipping_data.get("city"),
            postal_code=shipping_data.get("postalCode"),
            phone=shipping_data.get("phone"),
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            total_price += item.product.price * item.quantity

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
        if self.request.user.is_staff:
            return Order.objects.all().order_by('-created_at')
        
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
class MonthlyRevenueAPIView(APIView):
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