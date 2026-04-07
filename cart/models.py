from django.db import models
from django.contrib.auth import get_user_model
from products.models import ProductVariant

User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s cart"
    
from products.models import ProductVariant


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'variant')

    def __str__(self):
        return f"{self.variant} x {self.quantity}"
