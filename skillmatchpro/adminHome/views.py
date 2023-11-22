from .models import Category
from django.shortcuts import render, redirect
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
    # Fetch dispute details from the database using a stored procedure or view
    with connection.cursor() as cursor:
        cursor.callproc('GetDisputeDetails')  
        disputes = cursor.fetchall()
        columns = ["dispute_id", "dispute_by", "dispute_for", "project_id", "title", "content","type","date","dispute_status"]
        dispute = []
        for row in disputes:
            dispute.append(dict(zip(columns, row)))


    # Pass the disputes to the template
    return render(request, 'adminHome/dispute_details.html', context={'disputes': dispute})




