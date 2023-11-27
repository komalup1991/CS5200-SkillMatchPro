from django.urls import path
from . import views

urlpatterns = [
    path('raise-dispute/<int:project_id>/', views.RaiseDisputeView.as_view(), name='raise_dispute'),
    path('dispute/success/', views.dispute_success, name='dispute_success'),
]
