from django.shortcuts import render
from .models import UserInfo

def testmysql(request):
    users = UserInfo.objects.all()
    if users:
        user = users[0]
        context = {
            'user_id': user.userID,
            'user_name': user.name,
        }
    else:
        context = {
            'user_id': "1001",
            'user_name': "Group 4 Test User",
        }
    return render(request, 'home.html', context)
