from django.shortcuts import render, get_object_or_404
from .models import Bid, Project, Userinfo
from django.db.models import Sum, Max

def my_projects(request):
    # Get the logged-in user ID from the session
    user_id = request.session.get('user_id')

    if user_id:
        # Get the Userinfo instance for the logged-in user
        user_info = get_object_or_404(Userinfo, userid=user_id)

        if user_info.type == 'admin':
            # If the user is an admin, show all projects
            bid_projects = Bid.objects.all().order_by('-date')  # Order by date in descending order
            created_projects = Project.objects.all().order_by('-startdate')  # Order by startdate in descending order
        else:
            # If the user is not an admin, filter projects based on the logged-in user ID
            bid_projects = Bid.objects.filter(userid=user_info).order_by('-date')  # Order by date in descending order
            created_projects = Project.objects.filter(freelancerid=user_info).order_by('-startdate')  # Order by startdate in descending order
    else:
        # Handle the case where there is no logged-in user
        bid_projects = []
        created_projects = []
        
    if user_info.type == 'admin':
        path='myProjects/adminProjectView.html'
    else:
        path='myProjects/my_projects.html'
        
    return render(request, path, {
        'bid_projects': bid_projects,
        'created_projects': created_projects,
    })
