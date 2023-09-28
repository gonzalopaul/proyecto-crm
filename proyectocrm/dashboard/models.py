from django.db import models

# Create your models here.

CATEGORY = (
('Crystal Box', 'Crystal Box'),
('Crystal Bar', 'Crystal Bar'),
('2800 puff', '2800 puff'),
)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.name} - {self.quantity}'
