import requests
import json
from datetime import datetime
import base64
from requests.api import request
from requests.auth import HTTPBasicAuth

    
def getAccessToken(request):
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
    
    
    
def lipa_na_mpesa_online(request):
    access_token = getAccessToken(request)
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = { "Authorization": "Bearer "+str(access_token) ,"Content-Type": "application/json" }
    request = {
        "BusinessShortCode": Business_short_code,
        "Password": decode_password,
        "Timestamp":lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254702822379,  # replace with your phone number to get stk push
        "PartyB": Business_short_code,
        "PhoneNumber": 254702822379,  # replace with your phone number to get stk push
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

lipa_na_mpesa_online(request)