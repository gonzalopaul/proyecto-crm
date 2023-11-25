from django import forms
from .models import Product, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity']

class ProductForm2(forms.ModelForm):

    category_choices = [
        ('0% Nic 600 Puff', '0% Nic 600 Puff'),
        ('2% Nic 600 Puff', '2% Nic 600 Puff'),
        ('5% Nic 600 Puff', '5% Nic 600 Puff'),
    ]
    category = forms.ChoiceField(choices=category_choices, required=False)
    iva_rate = forms.FloatField(required=True)

    class Meta:
        model = Product
        fields = ['category', 'iva_rate']