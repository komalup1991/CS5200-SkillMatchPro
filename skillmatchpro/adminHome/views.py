from .models import Category
from django.shortcuts import render, redirect
from django.views import View



# Create your views here.


def home(request):
    categories = Category.objects.all()
    context = {'categories': categories} 
    return render(request, 'adminHomePage.html', context)





