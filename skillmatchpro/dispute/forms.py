from django import forms
from .models import Dispute

class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = ['type', 'content']
