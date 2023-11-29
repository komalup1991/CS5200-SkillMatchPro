from django.shortcuts import render, redirect, get_object_or_404
from .models import UserInfo, Profile, Project
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from .forms import UserRegisterForm, LoginForm, ProfileForm
from django.utils import timezone
from django.contrib import messages
from django.db import connection
from django.contrib.auth import authenticate, login
import uuid
import os


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
                authenticated_user = authenticate(request, username=name, password=password)
                login(request, authenticated_user)
                
                return redirect('custom-admin:admin-dashboard')

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
                # messages.success(request, f'Welcome, user {user.userID}!')
                if user.type == 'admin':
                    authenticated_user = authenticate(request, username=username, password=password)
                    login(request, authenticated_user)
                    return redirect('custom-admin:admin-dashboard')
                else:
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
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = UserInfo.objects.get(userID=user_id)
            except UserInfo.DoesNotExist:
                messages.error(request, 'User not found')
                return redirect('login')
            # get initial value for edit_profile form

            cursor = connection.cursor()
            cursor.execute('''select 
                                profilePicture,
                                firstName as FirstName,
                                lastName as LastName,
                                specialization as Specialization, 
                                bio as Bio
                            from UserInfo Join Profile on UserInfo.userID = Profile.userid
                            where UserInfo.userID = %s
                            ''', [user_id])

            user = cursor.fetchone()
            initial_dict = {
                "profilePicture": user[0],
                "firstName": user[1],
                "lastName": user[2],
                "specialization": user[3],
                "bio": user[4]
            }
    
            form = ProfileForm(initial=initial_dict)
            return render(request, "userInfo/edit_profile.html", {'form': form})
    
        else:
            messages.error(request, 'User not authenticated')
            return redirect('login')
        
    def post(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = UserInfo.objects.get(userID=user_id)
            except UserInfo.DoesNotExist:
                messages.error(request, 'User not found')
                return redirect('login')
       
            form = ProfileForm(request.POST, request.FILES)

        if user_id and form.is_valid():
            try:
                user = UserInfo.objects.get(userID=user_id)
            except UserInfo.DoesNotExist:
                messages.error(request, 'User not found')
                return redirect('login')

            # post to db
            # p = request.FILES.get("file") # the image object
            
            profile_picture = request.FILES.get('profilePicture')

            if profile_picture:
                # Generate a unique filename for the image
                unique_filename = str(uuid.uuid4()) + os.path.splitext(profile_picture.name)[-1]
                # abs_path = os.path.abspath(__file__)
                # abs_path = os.path.dirname(abs_path)

                image_directory = 'userInfo/static/profile/img/'
                image_path = os.path.join(image_directory, unique_filename)

                with open(image_path, 'wb') as f:
                    for chunk in profile_picture.chunks():
                        f.write(chunk)
                image_path = os.path.join('profile/img/', unique_filename)
            else:
                image_path = ''

            firstName = form.cleaned_data.get('firstName', "")
            lastName = form.cleaned_data.get('lastName', "")
            specialization = form.cleaned_data.get('specialization', "")
            bio = form.cleaned_data.get('bio', "")
            
            if image_path == "":
                Profile.objects.filter(userid=user_id).update(
                    firstname=firstName,
                    lastname=lastName,
                    bio=bio
                )
            else:
                Profile.objects.filter(userid=user_id).update(
                    profilepicture = image_path,
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
        cursor.execute('''select
                            profilePicture,
                            name as Username, 
                            firstName as FirstName,
                            lastName as LastName,
                            specialization as Specialization, 
                            rating as Rating,
                            bio as Bio,
                            UserInfo.userID
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
            'bio': user[6],
            'user_id': user[7]
        }
        return render(request, "userInfo/other_profile.html", context)

class OtherProjectsView(View):
    def get(self, request, user_id):

        cursor = connection.cursor()
        cursor.execute('''select * from Project
                        where freelancerID = %s
                        ''', [user_id])

        projects = cursor.fetchall()
        context = {
            "data": projects
        }
        return render(request, 'userInfo/other_projects.html', context)
