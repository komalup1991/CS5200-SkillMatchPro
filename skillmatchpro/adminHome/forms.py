# your_app_name/forms.py
from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(label='Enter your query')
