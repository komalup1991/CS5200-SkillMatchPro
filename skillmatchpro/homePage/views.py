from django.shortcuts import render
from django.db import connection

# Create your views here.
category_table = {
    "webDevelopment": 1,
    "marketing": 2,
    "clothes": 3,
    "ux": 4,
    "Copywriting": 5,
    "food": 6,
    "sport": 7,
    "backEnd": 8,
    "frontEnd": 9,
    "security": 10,
}


def postsOfCategory(request, category=''):
    if category not in category_table:
        return "Category Not Found"

    cursor = connection.cursor()
    category_id = category_table[category]
    cursor.execute('''SELECT title, startDate, name, photo, projectID
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.categoryID = %s
                    ORDER BY p.startDate DESC
                    ''', (category_id))
    projects = cursor.fetchall

    context = {
        'isHome': False,
        "data": projects
    }
    return render(request, 'homePage/homePage.html', context)


def lastestPost(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('''SELECT title, startDate, name, photo, projectID
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    ORDER BY p.startDate DESC
                    ''')
    projects = cursor.fetchall

    context = {
        "isHome": True,
        "data": projects,
    }
    return render(request, 'homePage/homePage.html', context)


def postsOfSearch(request):
    query = request.GET.get('q', '')
    cursor = connection.cursor()
    cursor.execute('''SELECT title,startDate, name, photo
                    FROM Project p
                    JOIN UserInfo u
                    ON p.freelancerID = u.userID
                    WHERE p.title LIKE %s
                    OR p.description LIKE %s
                    ORDER BY p.startDate DESC
                    ''', ('%' + query + '%', '%' + query + '%'))
    projects = cursor.fetchall

    context = {
        'isHome': False,
        "data": projects,
    }
    return render(request, 'homePage/homePage.html', context)


def demo(request):
    return render(request, 'homePage/designDemo.html')
