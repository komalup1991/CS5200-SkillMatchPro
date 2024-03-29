from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from project.models import Project  
from django.utils import timezone

def payment(request, project_id):
    current_time = timezone.now()
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payer_id = request.session.get('user_id')
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT freelancerID
                FROM Project
                WHERE projectID = %s
            """, [project_id])
            result = cursor.fetchone()

        if result:
            payee_id = result[0]
            payment_status = 'in_progress'
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Payment (payerID, payeeID, projectID, type, amount, paymentStatus, date)
                    VALUES (%s, %s, %s, 'offline', %s, %s, %s)
                """, [payer_id, payee_id, project_id, amount, payment_status, current_time])
            
            return redirect('payment_success')
        else:
            return HttpResponse("Freelancer ID not found for the given project ID.")

    return render(request, 'payments/payment_form.html', {'project_id': project_id})
    
def payment_success(request):
    return render(request, 'payments/payment_success.html')

def invoice(request, project_id):
     with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                i.projectID,
                pr.title,
                (SELECT name FROM UserInfo where userID=i.clientUserID) AS Client,
                (SELECT name FROM UserInfo where userID=i.freelancerUserID) AS FreeLancer,
                i.date,
                i.amount,
                i.invoiceID,
                s.trackingNumber
                
            FROM
                Invoice i JOIN Project pr ON i.projectID = pr.projectID
                JOIN Payment p 
                ON i.projectID= p.projectID AND i.paymentID=p.paymentID
                JOIN Shipping s
                ON s.projectID = i.projectID
             WHERE
                p.projectID = %s
        """, [project_id])

        invoice_data = cursor.fetchone()
        if invoice_data:
            context = {
                'project_id': invoice_data[0],
                'project_name': invoice_data[1],
                'client_name': invoice_data[2],
                'freelancer_name': invoice_data[3],
                'invoice_date': invoice_data[4],
                'total_amount': invoice_data[5],
                'invoice_id' : invoice_data[6],
                'tracking_no': invoice_data[7],
            }

            return render(request, 'payments/invoice.html', context)
        else:
            return render(request, 'error.html', {'error_message': 'Invoice not found'})
        return render(request, 'payments/invoice.html', {'project_id': project_id})
    


def payment_or_invoice(request, project_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT paymentStatus FROM Payment WHERE projectID = %s", [project_id])
        payment_status = cursor.fetchone()
    if payment_status and payment_status[0] == 'verified':
        return redirect('invoice', project_id=project_id)
    elif payment_status and payment_status[0] == 'in_progress':
        return render(request, 'payments/payment_success.html')
    else:
        return render(request, 'payments/payment_form.html', context={'project_id': project_id, 'payment_status': 'No payment record found'})