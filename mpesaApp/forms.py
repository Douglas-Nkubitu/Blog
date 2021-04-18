from django import forms

class MpesaForm(forms.Form):
    PhoneNumber = forms.CharField(label='Enter Phone Number e.g 254702822379')
    Amount = forms.IntegerField(label='Amount')

class QueryForm(forms.Form):
    Query = forms.CharField(label='Enter to Query by Phone Number,Transaction ID')

