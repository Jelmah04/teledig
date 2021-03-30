
import datetime
from django.conf import settings
import math, random
import requests


def generateOTP() : 
  
    # Declare a digits variable   
    # which stores all digits  
    digits = "0123456789"
    OTP = ""
  
   # length of password can be chaged 
   # by changing value in range 
    for i in range(5) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP


def fetch_data_plan(di):
    url = 'https://www.alexdata.com.ng/api/data/'
    headers = {
        "Authorization": "Token " +settings.ALEX_DATA_KEY,
        'Content-Type': 'application/json'
    }
    x = requests.get(url, headers=headers)
    return x



# TWILIO_AUTH_TOKEN = config('fd68b1d10da2eb3853938015794026a1')
# AC4947d9b81b370deb9024940b70b2c8a1
# 19d346e5f21547ca93bed98f32cb1e38
# 