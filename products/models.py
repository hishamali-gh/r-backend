from django.db import models
from django.core.exceptions import ValidationError


class ProductType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('MEN', 'MEN'),
        ('WOMEN', 'WOMEN'),
        ('KIDS', 'KIDS')
    )

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='items'
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            has_stock = self.variants.filter(stock__gt=0).exists()

            if not has_stock and self.is_active:
                raise ValidationError("Cannot activate product without stock")

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            sizes = self.product_type.sizes.all()

            if not sizes.exists():
                raise ValidationError("No sizes defined for this product type")

            for size in sizes:
                ProductVariant.objects.get_or_create(
                    product=self,
                    size=size,
                    stock=0
                )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    url = models.URLField()
    main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name}'s image"


class SizeOption(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='sizes'
    )
    value = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product_type', 'value'],
                name='unique_product_type_value'
            )
        ]
        ordering = ['value']

    def __str__(self):
        return f"{self.product_type.name} - {self.value}"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    size = models.ForeignKey(
        SizeOption,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    stock = models.PositiveIntegerField(default=0)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'size'],
                name='unique_product_size'
            )
        ]

    @property
    def final_price(self):
        return self.price if self.price else self.product.price

    def clean(self):
        if self.size.product_type != self.product.product_type:
            raise ValidationError("Size does not match product type")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        product = self.product

        has_stock = product.variants.filter(stock__gt=0).exists()

        if not has_stock:
            if product.is_active:
                product.is_active = False
                product.save(update_fields=['is_active'])

        else:
            if not product.is_active:
                product.is_active = True
                product.save(update_fields=['is_active'])

    def __str__(self):
        return f"{self.product.name} - {self.size.value}"
