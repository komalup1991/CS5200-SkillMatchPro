from django.db import connection


def getUserInfo(request):
    id = request.session.get('user_id')
    if id is None:
        return {
            "user": {0: 'nomral', 1: "profile/img/1ac7bac1-f230-4b39-a392-91f5b53e0970.jpeg"}
        }
    cursor = connection.cursor()
    cursor.execute('''SELECT profileType, profilePicture
                   FROM Profile
                   WHERE userID = %s
                   ''', (id))
    user = cursor.fetchone()

    return {
        "user": user
    }
