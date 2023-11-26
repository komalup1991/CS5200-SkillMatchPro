from django.shortcuts import render, redirect
from .models import Payment
from .forms import PaymentForm
from project.models import Project  

def payment(request, project_id):
    project = Project.objects.get(pk=project_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_data = form.cleaned_data
            payment = Payment(
                payer=request.user,
                payee=project.freelancerid, 
                project=projectid,
                type=payment_data['payment_type'],
                amount=payment_data['amount'],
            )
            payment.save()
            return redirect('payment_success')

    else:
        form = PaymentForm()

    return render(request, 'payments/payment_form.html', {'project_id': project_id, 'form': form})

def payment_success(request):
    return render(request, 'payments/payment_success.html')

def invoice(request, project_id):
    # Add logic to generate invoice and save it to the database
    return render(request, 'payments/invoice.html', {'project_id': project_id})
