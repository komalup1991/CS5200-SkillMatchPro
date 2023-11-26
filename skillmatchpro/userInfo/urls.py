from django.urls import path
from .views import Index, RegisterView, ProfileView, LoginView
from django.contrib.auth import views as auth_views # authentication view
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView.as_view(template_name='userInfo/logout.html'), name="logout"),
    path("profile/", login_required(ProfileView.as_view()), name="profile"),
]
