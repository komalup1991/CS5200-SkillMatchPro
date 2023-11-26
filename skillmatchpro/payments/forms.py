from django import forms

class PaymentForm(forms.Form):
    payment_type = forms.ChoiceField(choices=[('offline', 'Offline'), ('online', 'Online')])
    amount = forms.DecimalField(min_value=0.01, decimal_places=2, max_digits=10)
