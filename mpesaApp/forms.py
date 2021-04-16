from django import forms

class MpesaForm(forms.Form):
    PhoneNumber = forms.CharField(label='Phone Number')
    Amount = forms.IntegerField(label='Amount')
