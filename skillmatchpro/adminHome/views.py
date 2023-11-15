from .models import Category
from django.shortcuts import render, redirect
from django.views import View
from langchain import  ConversationChain, LLMChain, PromptTemplate
from langchain import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import AzureOpenAI
from langchain.memory import ConversationEntityMemory
#from langchain.chains.conversation.memory import ConversationBufferMemory,ConversationBufferWindowMemory,ConversationSummaryMemory
import time
import os
import openai
from langchain_experimental.sql import SQLDatabaseChain
from langchain import OpenAI,SQLDatabase#,ConversationBufferWindowMemory
from .forms import QueryForm  


openai_api_key = "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"



endpoint_url = '35.197.100.91'
database = 'skillpromatch'
user = 'Komal'
password = ""
table_name = "Project"

db_uri = f"mysql+pymysql://{user}:{password}@{endpoint_url}/{database}"
db = SQLDatabase.from_uri(db_uri,include_tables=["Project","Bid"])
llm = OpenAI(openai_api_key=openai_api_key, temperature=0, verbose=True)
memory = ConversationBufferMemory(k=5)

db_chain = SQLDatabaseChain.from_llm(llm, db, memory=memory, verbose=True, top_k=5)



# Create your views here.
def query_result(request):
    form = QueryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        query = form.cleaned_data['query']
        
        # Run the query using db_chain
        query_result =db_chain.run(query)

        # Assuming you have a template named 'result.html'
        return render(request, 'adminHome/result.html', {'query_result': query_result, 'form': form})

    return render(request, 'adminHome/result.html', {'form': QueryForm()})
    #return redirect('custom-admin')

def home(request):
    categories = Category.objects.all()
    context = {'categories': categories} 
    return render(request, 'adminHomePage.html', context)





