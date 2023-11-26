from django.urls import path
from . import views as views

urlpatterns = [
    path('',views.ProjectList.as_view(), name='project_list' ),
    path('projectlist/', views.ProjectList.as_view(), name='project_list'),
    path('projectlist/<int:project_id>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('bid/<int:project_id>/<str:max_bid>', views.bidAdd, name='bid_form'),
    path('projectlist/add',views.ProjectAdd,name='project_add'),
]
