
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

    path("", include("userInfo.urls")),
    path("home/", homePage_views.lastestPost, name='home'),
    path("category/<str:category>",
         homePage_views.postsOfCategory, name='category-page'),
    path("send/<int:id>", message_views.send_message, name='send'),
    path("message/", message_views.message, name='message'),
    path('my-projects/', myProject_views.my_projects, name='my-projects'),
    path('custom-admin/', custom_admin_site.urls, name='custom-admin'),
    path("search/", homePage_views.postsOfSearch, name='search'),

    path('project/', include('project.urls')),
    path('user/', include("userInfo.urls")),
    path('adminHome/', include('adminHome.urls')),
    path('payments/', include('payments.urls')),
]
