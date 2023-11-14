from django.shortcuts import render, get_object_or_404
from .models import Bid, Project

def my_projects(request):
    bid_projects = Bid.objects.all()
    created_projects = Project.objects.all()

    return render(request, 'myprojects/my_projects.html', {
        'bid_projects': bid_projects,
        'created_projects': created_projects,
    })



