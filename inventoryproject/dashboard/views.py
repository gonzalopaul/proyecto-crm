from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest


# Create your views here.

def generate_pdf(request):
    # Obtener los datos de la base de datos para el usuario actual
    user_orders = Order.objects.filter(staff=request.user)

    # Calcular la suma de order_quantity y el precio total
    total_quantity = sum(order.order_quantity for order in user_orders)
    static_price = 5  # Número estático para el precio por unidad
    total_price = sum(order.order_quantity * static_price for order in user_orders)

    # Calcular el IVA (21%)
    iva_rate = 0.21
    iva_amount = total_price * iva_rate

    # Crear un objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orders.pdf"'

    # Crear el objeto Canvas del PDF
    p = canvas.Canvas(response)

    logo_path = 'media/logos/1.png'  # Ruta a tu archivo de logo
    p.drawImage(logo_path, 50, 750, width=100, height=100)  # Ajusta las coordenadas y dimensiones según sea necesario
    p.setFont("Helvetica", 20)
    p.drawCentredString(300, 790, "FACTURA")

    # Datos de la empresa
    p.setFont("Helvetica", 10)
    p.drawString(55, 747, "Foodrifish Import - Export")
    p.drawString(55, 735, "Avd. General Duque de")
    p.drawString(55, 723, "Aveiro, 7 29140")
    p.drawString(55, 711, "Malaga, España")
    p.drawString(55, 699, "NIF: B42755314")
    # Añadir la fecha actual a la factura
    # Obtener la fecha actual
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p.setFont("Helvetica", 10)
    p.drawString(350, 747, f"Fecha de emisión: {current_date}")

    # Calcular el ancho del documento
    width, height = letter
    table_width = 400  # Ancho deseado de la tabla

    x_position = 55
    y_position = 500

    # Datos de la tabla
    table_data = [['Order ID', 'Product','Category','Units','Price']]
    for order in user_orders:
        order_price = order.order_quantity * static_price  # Calcular el precio
        table_data.append([str(order.id), order.product.name, order.product.category, order.order_quantity,f"{order_price:.2f} €"])

    # Agregar separador entre productos y precio
    table_data.append(['', '', '', '', ''])
    # Agregar la fila de suma al final de la tabla
    table_data.append(['', '', 'TOTAL', total_quantity, f"{total_price:.2f} €"])

    # Agregar la fila de IVA a la tabla
    table_data.append(['', '', '', 'IVA (21%)',  f"{iva_amount:.2f} €"])

    # Agregar la fila de precio total con IVA a la tabla
    total_price_with_iva = total_price + iva_amount
    table_data.append(['', '', '', 'Precio Total con IVA', f"{total_price_with_iva:.2f} €"])


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

    # Calcular la altura de la tabla
    table_height = table.wrapOn(p, table_width, 400)

    # Ajustar la posición del pie de página debajo de la tabla
    footer_y_position = 300

    # Añadir el pie de página
    p.setFont("Helvetica", 10)
    p.drawString(55, footer_y_position, "¡Gracias por tu compra! Procesaremos tu pedido una vez hayamos recibido el pago")

    # Información de contacto
    p.drawString(55, footer_y_position - 15, "Síguenos en Instagram: @solopods_")
    p.drawString(55, footer_y_position - 30, "Correo Electrónico: iglobalstore00@gmail.com")
    p.drawString(55, footer_y_position - 45, "Teléfono: +34 606656761")

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

@login_required
def confirm_order(request, pk):
    order = get_object_or_404(Order, id=pk)

    if request.method == 'POST':
        order.confirmed = True
        order.save()

        product = order.product
        if order.order_quantity <= product.quantity:
            product.quantity -= order.order_quantity
            product.save()
            messages.success(request, f'Order {order.id} has been confirmed successfully.')
            return redirect('dashboard-order')
        else:
            return HttpResponseBadRequest("Not enough quantity in stock.")

    elif request.method == 'GET':
        # Aquí puedes manejar la lógica para mostrar detalles de la orden antes de confirmar
        context = {
            'order': order,
        }
        return render(request, 'dashboard/confirm_order.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method")