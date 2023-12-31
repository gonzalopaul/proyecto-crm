from django.urls import path
from . import views
from .views import generate_pdf
from django.views.generic import TemplateView


urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('staff/detail/<int:pk>/', views.staff_detail, name='dashboard-staff-detail'),
    path('product/', views.product, name='dashboard-product'),
    path('product/staff/', views.product_staff, name='dashboard-product-staff'),
    path('product/delete/<int:pk>/', views.product_delete, name='dashboard-product-delete'),
    path('product/update/<int:pk>/', views.product_update, name='dashboard-product-update'),
    path('order/', views.order, name='dashboard-order'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('order/confirm/<int:pk>/', views.confirm_order, name='confirm-order'),
    path('iva/', views.update_iva_rate, name='update-iva-rate'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete-order'),
]