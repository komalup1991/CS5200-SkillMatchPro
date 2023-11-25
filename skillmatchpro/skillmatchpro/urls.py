
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
from homePage import views as homePage_views
from message import views as message_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', homePage_views.demo),
    path("home/", homePage_views.lastestPost, name='home'),
    path("category/<str:category>",
         homePage_views.postsOfCategory, name='category-page'),
    path("search/", homePage_views.postsOfSearch, name='search'),
    path("send/<int:id>", message_views.send_message, name='send'),
    path("message/", message_views.message, name='message'),
]
