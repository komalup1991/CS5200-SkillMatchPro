from django.urls import path
from .views import Index, RegisterView, ProfileView, LoginView, EditProfileView, ProfileList, OtherProfileView, OtherProjectsView
from django.contrib.auth import views as auth_views # authentication view
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", LoginView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView.as_view(template_name='userInfo/logout.html'), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("edit_profile/", EditProfileView.as_view(), name="edit_profile"),
    path("profile_list/", ProfileList.as_view(), name="profile_list"),
    path("other_profile/<int:user_id>", OtherProfileView.as_view(), name="other_profile"),
    path("other_projects/<int:user_id>", OtherProjectsView.as_view(), name="other_projects")
]
