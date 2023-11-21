
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
from userInfo import views as userInfo_views
# from homePage import views as homePage_views
from myProjects import views as myProject_views
from adminHome import views as adminHomePage_views
from adminHome.admin import custom_admin_site


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', homePage_views.demo),
    path("home/", homePage_views.lastestPost, name='home'),
    path("category/<str:category>",
         homePage_views.postsOfCategory, name='category-page'),
    path("search/", homePage_views.postsOfSearch, name='search'),
    # path("home/", homePage_views.testHomePage),
    path('my-projects/', myProject_views.my_projects, name='my-projects'),
    path('query/', adminHomePage_views.query_result, name='query_result'),
    # path('admin/dashboard', custom_admin_site.dashboard_view, name='admin-dashboard'),
    path('custom-admin/', custom_admin_site.urls, name='custom-admin')

    # http://127.0.0.1:8000/custom-admin/dashboard/
]
