from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:project_id>/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('invoice/<int:project_id>/', views.invoice, name='invoice'),
]
