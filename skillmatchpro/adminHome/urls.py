from django.urls import path
from . import views as views

urlpatterns = [
    path('query/', views.query_result, name='query_result'),
    path('message_details/', views.message_details,name='message_details'),
    path('dispute_details/<int:dispute_id>/',views.dispute_detail_view, name='dispute_detail_view'),
    path('dispute_details/', views.dispute_details,name='dispute_details'),
    path('settling_dispute/', views.settling_dispute_view,name='settling_dispute_view'),
    path('resolve_ind/<int:dispute_id>/',views.resolve_ind_views, name='resolve_ind_views'),
    path('payment_details/<int:payment_id>/',views.payment_detail_view, name='payment_detail_view'),
    path('payment_details/', views.payment_details,name='payment_details'),
    path('shipping_details/<int:shipping_id>/',views.shipping_detail_view, name='shipping_detail_view'),
    path('shipping_details/', views.shipping_details,name='shipping_details'),
    path('resolve_payment/<int:payment_id>/',views.resolve_payment, name='resolve_payment'),
]