from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image,  SimpleDocTemplate, Table, TableStyle, Image


# Create your views here.

def generate_pdf(request):
    # Obtener los datos de la base de datos para el usuario actual
    user_orders = Order.objects.filter(staff=request.user)

    # Calcular la suma de order_quantity y el precio total
    total_quantity = sum(order.order_quantity for order in user_orders)
    static_price = 5  # Número estático para el precio por unidad
    total_price = sum(order.order_quantity * static_price for order in user_orders)


    # Crear un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orders.pdf"'

    # Crear el objeto Canvas del PDF
    p = canvas.Canvas(response)

    logo_path = 'media/logos/1.png'  # Ruta a tu archivo de logo
    p.drawImage(logo_path, 50, 750, width=100, height=100)  # Ajusta las coordenadas y dimensiones según sea necesario
    p.setFont("Helvetica", 14)
    p.drawCentredString(300, 800, "Factura del pedido")

    # Espaciado después del encabezado
    p.drawString(100, 710, "Productos seleccionados:")
    p.drawString(100, 705, "-" * 80)

    # Calcular el ancho del documento
    width, height = letter
    table_width = 400  # Ancho deseado de la tabla

    x_position = 55
    y_position = 600

    # Datos de la tabla
    table_data = [['Order ID', 'Product','Category','Units','Price']]
    for order in user_orders:
        order_price = order.order_quantity * static_price  # Calcular el precio
        table_data.append([str(order.id), order.product.name, order.product.category, order.order_quantity,order_price])

    # Agregar la fila de suma al final de la tabla
    table_data.append(['', '', 'TOTAL', total_quantity, total_price])

    # Crear la tabla
    table = Table(table_data, colWidths=[80, 100])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige)]))

    # Dibujar la tabla en el PDF
    table.wrapOn(p, table_width, 400)
    table.drawOn(p, x_position, y_position)
    p.save()
    return response

@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orders_count = orders.count()
    product_count = products.count()
    workers_count = User.objects.all().count()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'product_count': product_count,
        'workers_count': workers_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    context = {
        'workers': workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def staff_detail(request, pk):
    workers = User.objects.get(id=pk)
    context = {
        'workers': workers,
    }
    return render(request, 'dashboard/staff_detail.html', context)

@login_required
def product(request):
    items = Product.objects.all() # Using ORM
    product_count = items.count()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-product')
    else:
        form = ProductForm()
    context = {
        'items': items,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/product.html', context)


def product_staff(request):
    items = Product.objects.all()

    context = {
        'items': items,
    }
    return render(request, 'dashboard/product_staff.html', context)
@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')

@login_required
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method=='POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/product_update.html', context)

@login_required
def order(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count()
    product_count = Product.objects.all().count()
    context = {
        'orders': orders,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/order.html', context)