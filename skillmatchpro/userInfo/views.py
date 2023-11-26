from django.shortcuts import render, redirect
from .models import UserInfo, Profile
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from .forms import UserRegisterForm, LoginForm, ProfileForm
from django.utils import timezone
from django.contrib import messages
from django.db import connection


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
                messages.success(request, f'Welcome, user {user.userID}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
                return render(request, "userInfo/login.html", {'form': form})


class ProfileView(View):
    def get(self, request):
        # Retrieve user ID from the session
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = UserInfo.objects.get(userID=user_id)
            except UserInfo.DoesNotExist:
                messages.error(request, 'User not found')
                return redirect('login')
            
            cursor = connection.cursor()
            cursor.execute('''select profilePicture,
                                UserInfo.userID as UserID, 
                                name as Username, 
                                email as Email, 
                                firstName as FirstName,
                                lastName as LastName,
                                specialization as Specialization, 
                                rating as Rating,
                                type as UserType,
                                bio as Bio
                            from UserInfo Join Profile on UserInfo.userID = Profile.userid
                            where UserInfo.userID = %s
                            ''', [user_id])
                            
            user = cursor.fetchone()
            context = {
                'picture': user[0],
                'id': user[1],
                'username': user[2],
                'email': user[3],
                'fname': user[4],
                'lname': user[5],
                'specialization': user[6],
                'rating': user[7],
                'type': user[8],
                'bio': user[9]
            }
            return render(request, "userInfo/profile.html", context)
        
        else:
            messages.error(request, 'User not authenticated')
            return redirect('login')


class EditProfileView(View):
    def get(self, request):
        form = ProfileForm()
        return render(request, "userInfo/edit_profile.html", {'form': form})
    
    def post(self, request):
        user_id = request.session.get('user_id')
        form = ProfileForm(request.POST)

        if user_id and form.is_valid():
            try:
                user = UserInfo.objects.get(userID=user_id)
            except UserInfo.DoesNotExist:
                messages.error(request, 'User not found')
                return redirect('login')
            
            # to update the db tables: both userInfo and Profile
            picture = form.cleaned_data.get('profilePicture', False)
            firstName = form.cleaned_data.get('firstName', "")
            lastName = form.cleaned_data.get('lastName', "")
            specialization = form.cleaned_data.get('specialization', "")
            bio = form.cleaned_data.get('bio', "")

            Profile.objects.filter(userid=user_id).update(
                profilepicture =picture,
                firstname = firstName,
                lastname = lastName,
                bio = bio
            )
            UserInfo.objects.filter(userID=user_id).update(
                specialization = specialization
            )

        else:
            messages.error(request, 'User not authenticated')
            return redirect('login')

        return redirect('profile')

# using raw query to retrieve data
class ProfileListView(View):
    def get(self, request):
        # users = UserInfo.objects.all()
        # context = {
        #     "data": users
        # }
        # return render(request, 'profile_list', context)
        cursor = connection.cursor()
        cursor.execute('''select name as Username, userID FROM UserInfo''')
        users = cursor.fetchall()
        context = {
            "data": users
        }
        return render(request, 'profile_list', context)

# using list view
class ProfileList(ListView):
    template_name = 'userInfo/profile_list.html'
    model = UserInfo

# to view other people's profile
class OtherProfileView(View):
    def get(self, request, user_id):
        cursor = connection.cursor()
        cursor.execute('''select profilePicture,
                            name as Username, 
                            firstName as FirstName,
                            lastName as LastName,
                            specialization as Specialization, 
                            rating as Rating,
                            bio as Bio
                        from UserInfo Join Profile on UserInfo.userID = Profile.userid
                        where UserInfo.userID = %s
                        ''', [user_id])

        user = cursor.fetchone()
        context = {
            'picture': user[0],
            'username': user[1],
            'fname': user[2],
            'lname': user[3],
            'specialization': user[4],
            'rating': user[5],
            'bio': user[6]
        }
        return render(request, "userInfo/other_profile.html", context)
