from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from project.models import Project  

def payment(request, project_id):
    if request.method == 'POST':
        # Retrieve form data
        amount = request.POST.get('amount')
        # Get the authenticated user's ID
        payer_id = request.session.get('user_id')
        payee_id = '2'  #replace with freelancer id from project
        # Set the payment status to 'in_progress'
        payment_status = 'in_progress'
        # Execute raw SQL query to insert payment record
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Payment (payerID,payeeID, projectID, type, amount, paymentStatus, date)
                VALUES (%s, %s, %s, 'offline', %s, %s, NOW())
            """, [payer_id, payee_id,project_id, amount, payment_status])

       

        # Redirect to a success page or the project details page
        return redirect('payment_success')

    # Render the payment form template for GET requests
    return render(request, 'payments/payment_form.html', {'project_id': project_id})


def payment_success(request):
    return render(request, 'payments/payment_success.html')

def invoice(request, project_id):
    # Add logic to generate invoice and save it to the database
    return render(request, 'payments/invoice.html', {'project_id': project_id})
