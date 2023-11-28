from django import forms
from .models import Dispute

class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = ['type', 'content']

    def __init__(self, *args, **kwargs):
        super(DisputeForm, self).__init__(*args, **kwargs)
        default_type = 'payment_issues'
        default_content = 'Enter your issues here...'

        self.initial['type'] = default_type
        self.initial['content'] = default_content
        self.fields['content'].widget = forms.Textarea(attrs={'rows': 4, 'cols': 25})

