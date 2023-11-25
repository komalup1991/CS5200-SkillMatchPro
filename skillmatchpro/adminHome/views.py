from .models import Category
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from langchain.prompts import  PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import AzureOpenAI
from langchain.memory import ConversationEntityMemory
import time
import os
import openai
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from .forms import QueryForm  
from django.db import connection
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferWindowMemory
from django.db import connections
from django.http import Http404
from django.http import HttpResponse




openai_api_key = "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"



endpoint_url = '35.197.100.91'
database = 'skillpromatch'
user = 'Komal'
password = ""
table_name = "Project"

db_uri = f"mysql+pymysql://{user}:{password}@{endpoint_url}/{database}"
db = SQLDatabase.from_uri(db_uri,include_tables=["Project","Bid","Category","Dispute","Invoice","Payment","Profile","Rating","Shipping","UserInfo"])
llm = OpenAI(openai_api_key=openai_api_key, temperature=0, verbose=True)
memory = ConversationBufferMemory(k=10)

db_chain = SQLDatabaseChain.from_llm(llm, db, memory=memory, verbose=True, top_k=20)



# Create your views here.
def query_result(request): 
    form = QueryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        query = form.cleaned_data['query']
        query_result =db_chain.run(query)
        return render(request, 'adminHome/result.html', {'query_result': query_result, 'form': form})
    return render(request, 'adminHome/result.html', {'form': QueryForm()})

def home(request):
    categories = Category.objects.all()
    context = {'categories': categories} 
    return render(request, 'adminHomePage.html', context)

def message_details(request):
    # Fetch message details from the database using a stored procedure or view
    with connection.cursor() as cursor:
        cursor.callproc('GetMessageDetails')  
        messages = cursor.fetchall()
        columns = ["message_id", "from_user", "to_user", "project_id", "title", "content","type","date"]
        m = []
        for row in messages:
            m.append(dict(zip(columns, row)))

    # Pass the messages to the template
    return render(request, 'adminHome/message_details.html', context={'messages': m})

def dispute_details(request):
    with connection.cursor() as cursor:
        cursor.callproc('GetDisputeDetails')  
        disputes = cursor.fetchall()
        columns = ["dispute_id", "dispute_by", "dispute_for", "project_id", "title", "content","type","date","dispute_status"]
        dispute = []
        for row in disputes:
            dispute.append(dict(zip(columns, row)))

    return render(request, 'adminHome/dispute_details.html', context={'disputes': dispute})


def resolve_ind_views(request, dispute_id):
    with connection.cursor() as cursor:
        try:
            print(f"Error ")
            cursor.callproc('settleDispute', [dispute_id])
        except Exception as e:
            print(f"Error executing stored procedure: {e}")

    # Add any additional logic or redirection as needed
    # Redirect to a different view or URL after settling the dispute
    return redirect('dispute_detail_view', dispute_id=dispute_id)





        
def settling_dispute_view(request):
    if request.method == 'POST':
        dispute_ids = request.POST.getlist('dispute_ids[]')
        
        for disputeID in dispute_ids:
            with connection.cursor() as cursor:
                cursor.callproc('settleDispute', [disputeID])
        
        # Redirect to the admin dashboard or another appropriate page
        return HttpResponseRedirect(reverse('custom-admin:admin-dashboard'))

    else:
        with connection.cursor() as cursor:
            cursor.callproc('GetAllDisputes')  # Uncomment this line to fetch all disputes
            all_disputes = cursor.fetchall()
            columns = ["dispute_id", "dispute_by", "dispute_for", "project_id", "title", "content", "type", "date", "dispute_status"]
            disputes = []
            for row in all_disputes:
                disputes.append(dict(zip(columns, row)))

        return render(request, 'adminHome/settling_dispute.html', {'all_disputes': disputes})


def dispute_detail_view(request, dispute_id):
    with connections['default'].cursor() as cursor:
        sql_query = "SELECT * FROM Dispute WHERE disputeID = %s"
        cursor.execute(sql_query, [dispute_id])
        dispute_data = cursor.fetchone()
    if not dispute_data:
        raise Http404("Dispute not found")
    dispute = {
        'dispute_id': dispute_data[0],
        'date': dispute_data[1],
        'type': dispute_data[2],
        'content': dispute_data[3],
        'dispute_by': dispute_data[4],  
        'dispute_for': dispute_data[5],
        'project_id': dispute_data[6],
        'status': dispute_data[7],
    }
    return render(request, 'adminHome/indDispute_detail.html', {'dispute': dispute})

def payment_detail_view(request, payment_id):
    with connections['default'].cursor() as cursor:
        sql_query = "SELECT * FROM Payment WHERE paymentID = %s"
        cursor.execute(sql_query, [payment_id])
        payment_data = cursor.fetchone()
    if not payment_data:
        raise Http404("Payment not found")
    payment = {
        'paymentID': payment_data[0],
        'payerID': payment_data[1],
        'payeeID': payment_data[2],
        'projectID': payment_data[3],
        'type': payment_data[4],  
        'amount': payment_data[5],
        'date': payment_data[6],
    }
    return render(request, 'adminHome/payment.html', {'payment': payment})

def payment_details(request):
    with connection.cursor() as cursor:
        cursor.callproc('GetPaymentDetails')  
        payments = cursor.fetchall()
        columns = ["payment_id", "payer", "payee", "projectID", "type", "amount","date"]
        payment = []
        for row in payments:
            payment.append(dict(zip(columns, row)))

    return render(request, 'adminHome/payment_details.html', context={'payments': payment})   

def shipping_detail_view(request, shipping_id):
    with connections['default'].cursor() as cursor:
        sql_query = "SELECT * FROM Shipping WHERE shippingID = %s"
        cursor.execute(sql_query, [shipping_id])
        shipping_data = cursor.fetchone()
    if not shipping_data:
        raise Http404("Shipping Details not found")
    shipping = {
        'shippingID': shipping_data[0],
        'projectID': shipping_data[1],
        'trackingNumber': shipping_data[2],  
        'date': shipping_data[3],
    }
    return render(request, 'adminHome/shipping.html', {'shipping': shipping})

def shipping_details(request):
    with connection.cursor() as cursor:
        cursor.callproc('GetShippingDetails')  
        shipments = cursor.fetchall()
        columns = ["shipping_id","projectID","tracking_no","date"]
        shipment = []
        for row in shipments:
            shipment.append(dict(zip(columns, row)))

    return render(request, 'adminHome/shipping_details.html', context={'shipments': shipment})   