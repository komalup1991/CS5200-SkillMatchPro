from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# inherits from the UserCreationForm
class UserRegisterForm(UserCreationForm):
    # username and password already included
    # fields
    is_admin = forms.BooleanField(required=False, initial=False, label="Register as Admin")
    admin_token = forms.CharField(required=False, label="Admin Token")
    email = forms.EmailField()

    class Meta:
        model = User
        # password1 for new password, password2: confirm
        fields = ['username', 'email', 'password1', 'password2', 'is_admin', 'admin_token']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class ProfileForm(forms.Form):
    profilePicture = forms.ImageField(required=False)
    firstName = forms.CharField(max_length=100)
    lastName = forms.CharField(max_length=100)
    specialization = forms.CharField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
