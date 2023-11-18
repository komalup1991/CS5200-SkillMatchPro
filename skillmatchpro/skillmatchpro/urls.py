
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
from django.urls import path
from userInfo import views as userInfo_views
from homePage import views as homePage_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', userInfo_views.testmysql),
    path("home/", homePage_views.lastestPost, name='home'),
    path("webDevelopment/", homePage_views.webDevPost, name='webDevelopment'),
    path("marketing/", homePage_views.marketPost, name='marketing'),
    path("clothes/", homePage_views.clothPost, name='clothes'),
    path("ux/", homePage_views.uxPost, name='ux'),
    path("copyRight/", homePage_views.copyPost, name='copy'),
    path("food/", homePage_views.foodPost, name='food'),
    path("sport/", homePage_views.sportPost, name='sport'),
    path("backEnd/", homePage_views.backPost, name='backEnd'),
    path("frontEnd/", homePage_views.frontPost, name='frontEnd'),
    path("security/", homePage_views.securitytPost, name='security'),


]
