from django.db import models
from django.contrib.auth import get_user_model
from products.models import ProductVariant

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('OTW', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    name = models.CharField(max_length=255)
    address = models.TextField(default='Thamarassery')
    city = models.CharField(max_length=100, default='Kozhikode')
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='order_items'
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.variant.product.name} ({self.variant.size.value}) x {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity
