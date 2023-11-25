from django.shortcuts import render
from django.db import connection
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def message(request):
    user_id = request.GET.get('user', '')
    project_id = request.GET.get('project', '')
    cursor = connection.cursor()
    cursor.execute('''select fromUserID, projectID, content, type, date, messageID, toUserID
                    from Message
                    where toUserID = %s
                    order by date desc
                    ''', (user_id))
    received_message = cursor.fetchall()

    context = {
        "data": received_message,
        "count": len(received_message),
        "id": user_id,
        "project_id": project_id,
    }
    return render(request, 'message.html', context)


@csrf_exempt
def send_message(request, id=""):
    if request.method == 'POST':
        to_user_id = request.POST.get('to_user_id')
        from_user_id = id
        project_id = request.POST.get('project_id')
        message_type = request.POST.get('message_type')
        message_content = request.POST.get('message_content')
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT userID FROM UserInfo WHERE userID = %s''', (to_user_id))
        user_info = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT projectID FROM Project WHERE projectID = %s''', (project_id))
        project_info = cursor.fetchall()

        if len(user_info) == 0 or len(project_info) == 0 or message_type == "":
            return JsonResponse({'status': 'error'})

        with connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO Message (toUserID, fromUserID, projectID, type, content, date)
                VALUES (%s, %s, %s, %s, %s, %s);
            ''', [to_user_id, from_user_id, project_id, message_type, message_content, date])

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})
