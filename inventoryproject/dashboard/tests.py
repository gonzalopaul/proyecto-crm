from django.contrib.auth.models import User
from .models import Product, Order
from django.urls import reverse
from django.test import TestCase, Client

class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(name="Test Product", category="0% Nic 600 Puff", quantity=10)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.category, "0% Nic 600 Puff")
        self.assertEqual(product.quantity, 10)

    def test_product_str_representation(self):
        product = Product.objects.create(name="Test Product", category="0% Nic 600 Puff", quantity=10)
        self.assertEqual(str(product), "Test Product-10")

class OrderModelTest(TestCase):
    def setUp(self):
        # Crear un usuario de ejemplo
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Crear un producto de ejemplo
        self.product = Product.objects.create(name="Test Product", category="0% Nic 600 Puff", quantity=10)

    def test_create_order(self):
        order = Order.objects.create(product=self.product, staff=self.user, order_quantity=5)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.staff, self.user)
        self.assertEqual(order.order_quantity, 5)
        self.assertFalse(order.confirmed)

    def test_order_str_representation(self):
        order = Order.objects.create(product=self.product, staff=self.user, order_quantity=5)
        expected_str = f'Test Product-10 ordered by testuser'
        self.assertEqual(str(order), expected_str)

class DashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Loguear al usuario
        self.client.login(username='testuser', password='testpassword')

        # Crear algunos productos y órdenes de prueba
        self.product = Product.objects.create(name='Test Product', category='0% Nic 600 Puff', quantity=10)
        self.order = Order.objects.create(product=self.product, staff=self.user, order_quantity=5)

    def test_index_view(self):
        url = reverse('dashboard-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_staff_view(self):
        url = reverse('dashboard-staff')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/staff.html')

    def test_product_view(self):
        url = reverse('dashboard-product')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/product.html')

    def test_order_view(self):
        url = reverse('dashboard-order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/order.html')

    def test_confirm_order_view(self):
        url = reverse('confirm-order', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/confirm_order.html')

    def test_generate_pdf_view(self):
        url = reverse('generate_pdf')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)