from django.shortcuts import render

# Create your views here.


def testHomePage(request):
    return render(request, 'homePage.html')


def lastestPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    ''')
    projects = cursor.fetchall

    context = {
        "data": projects
    }

    return render(request, 'homePage.html', context)


def webDevPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.categoryID = 1
                    ''')
    projects = cursor.fetchall

    context = {
        "data": projects
    }
    return render(request, 'categoryPage.html', context)


def marketPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.categoryID = 2
                    ''')
    projects = cursor.fetchall

    context = {
        "data": projects
    }
    return render(request, 'categoryPage.html', context)


def clothPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.categoryID = 3
                    ''')
    projects = cursor.fetchall

    context = {
        "data": projects
    }
    return render(request, 'categoryPage.html', context)


def uxPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.categoryID = 4
                    ''')
    projects = cursor.fetchall

    context = {
        "data": projects
    }
    return render(request, 'categoryPage.html', context)


def copyPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.categoryID = 5
                    ''')
    projects = cursor.fetchall

    context = {
        "data": projects
    }
    return render(request, 'categoryPage.html', context)


def foodPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.categoryID = 6
                    ''')
    projects = cursor.fetchall

    context = {
        "data": projects
    }
    return render(request, 'categoryPage.html', context)


def sportPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.categoryID = 7
                    ''')
    projects = cursor.fetchall

    context = {
        "data": projects
    }
    return render(request, 'categoryPage.html', context)


def backPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.categoryID = 8
                    ''')
    projects = cursor.fetchall

    context = {
        "data": projects
    }
    return render(request, 'categoryPage.html', context)


def frontPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.categoryID = 9
                    ''')
    projects = cursor.fetchall

    context = {
        "data": projects
    }
    return render(request, 'categoryPage.html', context)


def securitytPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.categoryID = 10
                    ''')
    projects = cursor.fetchall

    context = {
        "data": projects
    }
    return render(request, 'categoryPage.html', context)
