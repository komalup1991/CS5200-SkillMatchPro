from django.shortcuts import render, redirect
from .models import UserInfo
from django.views import View
from .forms import UserRegisterForm, LoginForm
from django.utils import timezone
from django.contrib.auth.hashers import check_password # for login
from django.contrib import messages


class Index(View):
    def get(self, request):
        return render(request, "userInfo/index.html")

# need to create form before making the view
class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        # add in the context: the key and value as a dictionary
        # will render in the templates
        return render(request, "userInfo/register.html", {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            # save in the database
            userid = UserInfo.objects.count()+1
            name = form.cleaned_data.get('username', '')
            email = form.cleaned_data.get('email', '')
            password = form.cleaned_data.get('password1', '')
            is_admin = form.cleaned_data.get('is_admin', False)
            admin_token = form.cleaned_data.get('admin_token', '')
            # to determine type of user
            if is_admin == True and admin_token == "admin":
                type = "admin"
            else:
                type = "normal"
            
            UserInfo.objects.create(userID = userid, name = name, email = email, password = password, type = type, registrationDate = timezone.now())


            if is_admin and admin_token =='admin':
                user = form.save()
                user.is_staff = True
                user.is_superuser = True
                user.save()
                return redirect('admin:index')

            return redirect('index')
        
        # If the form is not valid, re-render the form with validation errors
        else:
            return render(request, "userInfo/register.html", {'form': form})
        
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "userInfo/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')

            try:
                user = UserInfo.objects.get(name=username)
            except UserInfo.DoesNotExist:
                messages.error(request, 'Invalid credentials')
                return render(request, "userInfo/login.html", {'form': form})

            if password == user.password:
                request.session['user_id'] = user.userID  # Store user ID in the session
                messages.success(request, f'Welcome, {user.name}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid credentials')
                return render(request, "userInfo/login.html", {'form': form})

class ProfileView(View):
    def get(self, request):
        user = request.user
        user_info = UserInfo.objects.get(userID = user.id)
        return render(request, 'userInfo/profile.html', {'user_info': user_info})


