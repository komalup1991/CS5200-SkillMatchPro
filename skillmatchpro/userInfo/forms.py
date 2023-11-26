from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# inherits from the UserCreationForm
class UserRegisterForm(UserCreationForm):
    # username and password already included
    is_admin = forms.BooleanField(required=False, initial=False)
    admin_token = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))


# widget = forms.BooleanField(attrs={'class': 'form-check'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_admin', 'admin_token']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['is_admin'].widget.attrs['class'] = 'form-check'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class ProfileForm(forms.Form):
    profilePicture = forms.ImageField(required=False)
    firstName = forms.CharField(max_length=100)
    lastName = forms.CharField(max_length=100)
    specialization = forms.CharField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
