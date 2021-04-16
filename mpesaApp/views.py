from typing import ContextManager
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from requests.models import Request
from .models import Post
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Mpesa_Payments
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime
import base64
from requests.api import request
from .forms import MpesaForm



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'mpesaApp/home.html', context )

class PostListView(ListView):
    model = Post
    template_name = 'mpesaApp/home.html'
    context_object_name ='posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'mpesaApp/user_posts.html'
    context_object_name ='posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user). order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateview(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def getAccessToken():
        consumer_key = 'cyBzERd2PMFDXlA6tMzcWbGwiCBYSMtn'
        consumer_secret = 'Giq642DlHfpmum36'
        api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'      
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        return r.json()['access_token']


lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
Business_short_code = "174379"
passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
data_to_encode = Business_short_code + passkey + lipa_time
online_password = base64.b64encode(data_to_encode.encode())
decode_password = online_password.decode('utf-8')


def lipa_na_mpesa_online(Amount,PhoneNumber):
    access_token = getAccessToken()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = { "Authorization": "Bearer "+str(access_token) ,"Content-Type": "application/json" }
    request = {
        "BusinessShortCode": Business_short_code,
        "Password": decode_password,
        "Timestamp":lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": Amount,
        "PartyA": PhoneNumber,  # replace with your phone number to get stk push
        "PartyB": Business_short_code,
        "PhoneNumber": PhoneNumber,  # replace with your phone number to get stk push
        "CallBackURL": "https://navariapp.herokuapp.com/lipa_na_mpesa",
        "AccountReference": "Navari Limited",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request, headers=headers)
    print(response.text)

    # check response code for errors and return response
    if response.status_code > 299:
        return{
            "success": False,
            "message":"Sorry, something went wrong please try again later."
        },400

    # CheckoutRequestID = response.text['CheckoutRequestID']

    # Do something in your database e.g store the transaction or as an order
    # make sure to store the CheckoutRequestID to identify the tranaction in 
    # your CallBackURL endpoint.

    # return a response to your user
    return {
        "data": json.loads(response.text)
    },200


def Mpesa_Payments(request):

    if request.method == 'POST':
        form =MpesaForm(request.POST)
        if form.is_valid():

            PhoneNumber = form.cleaned_data['PhoneNumber']
            Amount = form.cleaned_data['Amount']

            lipa_na_mpesa_online(Amount,PhoneNumber)

    form = MpesaForm()         
    return render (request, 'mpesaApp/mpesa_payments_form.html', {'form':form } )

def payment(request):
    context = {
        'payments': Mpesa_Payments.objects.all()
    }
    return render(request,'mpesaApp/payment.html', context )

class Mpesa_PaymentsListView(ListView):
    model = Mpesa_Payments
    template_name = 'mpesaApp/payment.html'
    context_object_name ='payments'
    ordering = ['-created_at']

@csrf_exempt
@require_http_methods(["POST"])
def lipa_na_mpesa(request):
    try:
        req = json.loads(request.body.decode("utf-8"))
        payment = Mpesa_Payments()
        payment.MerchantRequestID = req['Body']['stkCallback']['MerchantRequestID']
        payment.CheckoutRequestID = req['Body']['stkCallback']['CheckoutRequestID']
        payment.Amount = req['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
        payment.MpesaReceiptNumber = req['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        payment.TransactionDate = req['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
        payment.PhoneNumber = req['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
        payment.save()
      
    except:
        pass
    return JsonResponse({})

def fetch_payments(request):
    payment_list = list(Mpesa_Payments.objects.values('id','MerchantRequestID','CheckoutRequestID','Amount','MpesaReceiptNumber','TransactionDate','PhoneNumber','Status'))
    return JsonResponse(payment_list,safe=False)