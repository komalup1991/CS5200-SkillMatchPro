from django.shortcuts import render, get_object_or_404
from .models import Bid, Project, Userinfo
from django.db.models import Sum,Max

def my_projects(request):
    # Get the logged-in user ID from the session
    user_id = request.session.get('user_id')
    # Get the Userinfo instance for the logged-in user
    user_info = get_object_or_404(Userinfo, userid=user_id)
    # Filter bid projects and created projects based on the logged-in user ID
    bid_projects = Bid.objects.filter(userid=user_info)    
    created_projects = Project.objects.filter(freelancerid=user_info)
    return render(request, 'myProjects/my_projects.html', {
         'bid_projects': bid_projects,
        'created_projects': created_projects,
    })
