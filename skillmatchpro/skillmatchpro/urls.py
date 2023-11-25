
"""skillmatchpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from homePage import views as homePage_views
from myProjects import views as myProject_views
from adminHome import views as adminHomePage_views
from adminHome.admin import custom_admin_site
from homePage import views as homePage_views
from message import views as message_views
# from adminHome import settling_dispute_view, dispute_detail_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', homePage_views.demo),
    path("home/", homePage_views.lastestPost, name='home'),
    path("category/<str:category>",
         homePage_views.postsOfCategory, name='category-page'),
    path("send/<int:id>", message_views.send_message, name='send'),
    path("message/", message_views.message, name='message'),
    path('my-projects/', myProject_views.my_projects, name='my-projects'),
    path('query/', adminHomePage_views.query_result, name='query_result'),
    path('custom-admin/', custom_admin_site.urls, name='custom-admin'),
    path('message_details/', adminHomePage_views.message_details,
         name='message_details'),
    path("search/", homePage_views.postsOfSearch, name='search'),

    path('dispute_details/<int:dispute_id>/',
         adminHomePage_views.dispute_detail_view, name='dispute_detail_view'),
    path('dispute_details/', adminHomePage_views.dispute_details,
         name='dispute_details'),
    path('settling_dispute/', adminHomePage_views.settling_dispute_view,
         name='settling_dispute_view'),
    path('resolve_ind/<int:dispute_id>/',
         adminHomePage_views.resolve_ind_views, name='resolve_ind_views'),
    path('payment_details/<int:payment_id>/',
         adminHomePage_views.payment_detail_view, name='payment_detail_view'),
    path('payment_details/', adminHomePage_views.payment_details,
         name='payment_details'),
    path('shipping_details/<int:shipping_id>/',
         adminHomePage_views.shipping_detail_view, name='shipping_detail_view'),
    path('shipping_details/', adminHomePage_views.shipping_details,
         name='shipping_details'),

    path('project/', include('project.urls')),


]
