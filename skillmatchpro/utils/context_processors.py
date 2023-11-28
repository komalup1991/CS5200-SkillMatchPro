from django.db import connection


def getUserInfo(request):
    id = request.session.get('user_id')
    cursor = connection.cursor()
    cursor.execute('''SELECT type, profilePicture
                   FROM UserInfo u
                   JOIN Profile p
                   on u.userID = p.userID
                   WHERE u.userID = %s
                   ''', (id))
    user = cursor.fetchone

    return {
        "user": user,
    }
