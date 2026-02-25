from django.db import models

class ProductType(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('MEN', 'MEN'),
        ('WOMEN', 'WOMEN'),
        ('KIDS', 'KIDS')
    )

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='items')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    url = models.URLField()
    main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name}'s image"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=5)
    stock = models.PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'size'],
                name='unique_product_size'
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.size}"
