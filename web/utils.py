
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