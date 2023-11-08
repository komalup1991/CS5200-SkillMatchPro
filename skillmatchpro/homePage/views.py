from django.shortcuts import render

# Create your views here.


def testHomePage(request):

    context = {'num': "12345"}
    return render(request, 'homePage.html', context)
