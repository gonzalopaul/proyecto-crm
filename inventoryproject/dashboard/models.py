from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY = (
    ('0% Nic 600 Puff', '0% Nic 600 Puff'),
    ('2% Nic 600 Puff', '2% Nic 600 Puff'),
    ('5% Nic 600 Puff', '5% Nic 600 Puff'),
    ('0% Nic 2800 Puff', '0% Nic 2800 Puff'),
    ('2% Nic 2800 Puff', '2% Nic 2800 Puff'),
    ('5% Nic 2800 Puff', '5% Nic 2800 Puff'),
    ('0% Nic 7000 Puff', '0% Nic 7000 Puff'),
    ('2% Nic 7000 Puff', '2% Nic 7000 Puff'),
    ('5% Nic 7000 Puff', '5% Nic 7000 Puff'),
    ('0% Nic 8000 Puff', '0% Nic 8000 Puff'),
    ('2% Nic 8000 Puff', '2% Nic 8000 Puff'),
    ('5% Nic 8000 Puff', '5% Nic 8000 Puff'),
)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)
    iva_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
        return f'{self.name}-{self.quantity}'

# Crear Order
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Order'

    def __str__(self):
        return f'{self.product} ordered by {self.staff.username}'
    
    confirmed = models.BooleanField(default=False)
