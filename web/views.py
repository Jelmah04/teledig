from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from .serializers import RegisterSerializer
from .forms import SignUpForm
import datetime
from decimal import Decimal
from datetime import timedelta
from datetime import datetime as dt
import os
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.core.mail import message, send_mail, EmailMultiAlternatives
import requests
import json
import random
import string
import secrets
from django.http import HttpResponseRedirect
from twilio.rest import Client

from .payment import init_payment
import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

def gen_token(length=64, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@$%-_"):
	return "".join([secrets.choice(charset) for _ in range(0, length)])

def gen_ref(length=12, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-"):
	return "".join([secrets.choice(charset) for _ in range(0, length)])

NUMERIC_CHARS = string.digits
STRING_LENGTH = 7

def generate_random_number(chars=NUMERIC_CHARS, length=STRING_LENGTH):
	return "".join(random.choice(chars) for _ in range(length))

today = datetime.date.today()


def home(request):
	if request.user.is_authenticated:
		return redirect('index')
	return render(request, 'index.html')

@login_required
def index(request):
	user_wallet = UserWallet.objects.get(user=request.user)
	pay_history = PayHistory.objects.filter(user=request.user).order_by('id').reverse()[:7]
	usernotification = UserNotification.objects.filter(user=request.user)
	context = {
		'user_wallet': user_wallet.amount,
		'prev_amt': user_wallet.prev_amount,
		'pay_history': pay_history,
		'notify': usernotification
	}
	return render(request, 'home.html', context)

@login_required
def notification(request):
	title = request.POST.get('title')
	message = request.POST.get('message')
	is_featured = request.POST.get('is_featured')
	return render(request, 'notification.html', context)


@login_required
def my_wallet(request):
	context = {
		'paystack_key': settings.PAYSTACK_PUBLIC_KEY
	}
	return render(request, 'my-wallet.html', context)

def signin(request):
	if request.user.is_authenticated:
		return redirect('index')
	return render(request, 'login.html')


def signin_ajax(request):
	if request.is_ajax():
		email = request.POST.get('email', None)
		password = request.POST.get('password', None)

		user = auth.authenticate(email=email, password=password)
		if user is not None:
			auth.login(request, user)
			response = {'success': 'Login Successfully. You will be redirect now.'}
			return JsonResponse(response)
		else:
			response = {'error': 'Error Email/Password. Try again.'}
			return JsonResponse(response)
	else:
		response = {'error': 'Check inputs and try again.'}
		return JsonResponse(response)


def check_mail_ajax(request):
	if request.is_ajax():
		email = request.GET.get('email', None)
		check_email = User.objects.filter(email=email).exists()
		if check_email == True:
			response = {'error': 'Email already exists.'}
			return JsonResponse(response)
		else:
			response = {'success': 'Cool'}
			return JsonResponse(response)
	else:
		response = {'error': 'Error Email Checking.'}
		return JsonResponse(response)
	

def check_username_ajax(request):
	if request.is_ajax():
		username = request.GET.get('username', None)
		check_username = User.objects.filter(username=username).exists()
		if check_username == True:
			response = {'error': 'Username already exists.'}
			return JsonResponse(response)
		else:
			response = {'success': 'This is cool.'}
			return JsonResponse(response)
	else:
		response = {'error': 'Error Username Checking.'}
		return JsonResponse(response)

def check_mobile_ajax(request):
	if request.is_ajax():
		mobile = request.GET.get('mobile', None)
		check_mobile = User.objects.filter(mobile=mobile).exists()
		if check_mobile == True:
			response = {'error': 'Mobile already exists.'}
			return JsonResponse(response)
		else:
			response = {'success': 'This is cool.'}
			return JsonResponse(response)
	else:
		response = {'error': 'Error Mobile Number Checking.'}
		return JsonResponse(response)


def register(request):
	return render(request, 'register.html')


def register_ajax(request):
	if request.is_ajax():
		form = SignUpForm(request.POST)
		print('form submitted')
		print(request.POST)
		if form.is_valid():
			print('this form is valid')
			form.save()
			obj = form.save()
			otp_code = generateOTP()
			mobile = obj.mobile
			site_name = settings.SITE_NAME
			full_name = obj.first_name + ' ' + obj.last_name

			# print('about to send otp')
			# sms_number = mobile[1:]
			# send_sms = client.messages.create(body='Hi' + 'Thanks for joining Telepalace. \n your OTP is:' + otp_code + '.',
			# from_ = '+13603299156',
			# to = '+234'+ sms_number)
			# print ('otp sent = '+ otp_code)

			# subject_file = os.path.join(settings.BASE_DIR, "mail/register/subject.txt")
			# subject = render_to_string(subject_file, {'name': obj.first_name, 'site_name': site_name})
			# from_email = settings.DEFAULT_EMAIL_SENDER
			# to_email = [obj.email]
# 
			# register_message_file = os.path.join(settings.BASE_DIR, "mail/register/body.txt")
			# register_message = render_to_string(register_message_file, {
														# 'first_name': obj.first_name, 'last_name': obj.last_name,
														# 'otp_code': otp_code, 'site_name': site_name,
													# })
# 
			# message = EmailMultiAlternatives(subject=subject, body=register_message, from_email=from_email, to=to_email)
# 
			# html_template = os.path.join(settings.BASE_DIR, "mail/register/body.html")
			# template = render_to_string(html_template, {
														# 'first_name': obj.first_name, 'last_name': obj.last_name,
														# 'otp_code': otp_code, 'site_name': site_name,
														# })
# 
			# message.attach_alternative(template, "text/html")
# 
			# message.send()
			UserSettings.objects.create(
				user=obj,
				verified_code=otp_code
			)
			# alert('Your OTP code is .....' + ' ' + otp_code)
			UserWallet.objects.create(user=obj, walletID=obj.mobile)
			response = {
				# 'success': 'Registration successful. Kindly enter the OTP sent to your email address. ['+obj.email+'] \n ['+otp_code+']', 
				'success': 'Registration successful. Kindly enter the OTP sent to your email address. ['+obj.email+']', 
				'otp': otp_code
			}
			return JsonResponse(response)
		else:
			# print('this form is not a valid one')
			response = {'error': 'We could not process your request. Try again.'}
			return JsonResponse(response)
	else:
		response = {'error': 'Please check all fields and try again.'}
		return JsonResponse(response)


def verifyAccount(request):
	return render(request, 'verify_account.html')


def confirm_email_ajax(request):
	if request.is_ajax():
		otp_code = request.POST.get('otp_code', None)
		if otp_code:
			check_code = UserSettings.objects.filter(verified_code=otp_code).exists()
			if check_code:
				# get_user = UserSettings.objects.get(verified_code=otp_code)
				get_settings = UserSettings.objects.get(verified_code=otp_code)
				instance = UserSettings.objects.filter(id=get_settings.id).update(account_verified=True, code_expired=True)
				# User.objects.filter(user=instance.user)
				if instance:
					response = {
								 'success': 'Account Verified Successfully' # response message
								}
					return JsonResponse(response) # return response as JSON
				else:
					response = {
								 'error': 'Error verifying Account. Try again.' # response message
								}
					return JsonResponse(response) # return response as JSON
			else:
				response = {
					'error': 'Error Code. Check and try again.'
				}
				return JsonResponse(response)
		else:
			response = { 'error': 'Please input code and try again.' }
			return JsonResponse(response)


def reset_password_email(request):
	if request.is_ajax():
		email = request.POST.get('email', None)
		check_email = User.objects.filter(email=email).exists()
		if check_email == False:
			response = {'error': 'Email does not exists.'}
			return JsonResponse(response)
		# Email exists if the above error is not been throw
		# Let us send the email to the user
		user = User.objects.get(email=email)
		# Let's call the generate function to generate our token
		token = gen_token()
		first_name = user.first_name
		last_name = user.last_name
		site_name = settings.SITE_NAME
		password_link = settings.SITE_URL+'forgot-password/reset_password/?signature='+token

		# Let's setup variable's to add to our template
		subject_file = os.path.join(settings.BASE_DIR, "mail/reset_password/subject.txt")
		subject = render_to_string(subject_file, {'name': first_name, 'site_name': site_name})
		from_email = settings.DEFAULT_EMAIL_SENDER
		to_email = [email]

		password_message_file = os.path.join(settings.BASE_DIR, "mail/reset_password/body.txt")
		password_message = render_to_string(password_message_file, {
													'first_name': first_name, 'last_name': last_name,
													'password_link': password_link, 'site_name': site_name,
												})

		message = EmailMultiAlternatives(subject=subject, body=password_message, from_email=from_email, to=to_email)

		html_template = os.path.join(settings.BASE_DIR, "mail/reset_password/body.html")
		template = render_to_string(html_template, {
													'first_name': first_name, 'last_name': last_name,
													'password_link': password_link, 'site_name': site_name,
													})

		message.attach_alternative(template, "text/html")

		message.send()
		UserPassToken.objects.create(user=user, token=token, sent=True)
		response = {'success': 'Check your email for instructions'}
		return JsonResponse(response)


def reset_pass(request):
	if request.is_ajax():
		token = request.POST.get('signature', None)
		check_token = UserPassToken.objects.filter(token=token).exists()
		if check_token == False:
			response = {'error': 'Link has been expired. Try again.'}
			return JsonResponse(response)
		# Token exists.
		user_token = UserPassToken.objects.get(token=token)
		password1 = request.POST.get('new_password1')
		password2 = request.POST.get('new_password2')

		upper_case = sum(1 for c in password1 if c.isupper())
		digits = sum(1 for c in password1 if c.isdigit())
		chars = sum(1 for c in password1 if not c.isalnum())
		length = len(password1)

		if password2 != password1:
			return JsonResponse({'error': 'Password mismatch. Try again.'})
		elif length < 4:
			return JsonResponse({'error': 'Password is too short. Try another'})
		elif not upper_case:
			return JsonResponse({'error': 'Password must contain at least one Uppercase.'})
		elif not digits:
			return JsonResponse({'error': 'Password must contain at least one number.'})
		elif not chars:
			return JsonResponse({'error': 'Password must contain at least one character.'})

		new_password = make_password(password1)
		user = User.objects.get(id=user_token.user.id)
		user.password = new_password
		user.save()
		UserPassToken.objects.filter(token=token).update(expired=True)
		response = {'success': 'Password Reset Successful'}
		return JsonResponse(response)
	return render(request, 'password_reset_change.html')



def change_password_ajax(request):
	if request.is_ajax():
		old_password = request.POST.get("old_password", None)
		new_password1 = request.POST.get("new_password1", None)
		new_password2 = request.POST.get("new_password2", None)
		user = request.user

		if user.check_password(old_password):
			# We declare some password verifications

			upper_case = sum(1 for c in new_password1 if c.isupper())
			digits = sum(1 for c in new_password1 if c.isdigit())
			chars = sum(1 for c in new_password1 if not c.isalnum())
			length = len(new_password1)

			# We throw error if the above are passed

			if new_password2 != new_password1:
				response = {"error": "Password mismatch. Try again."}
			elif length < 6:
				response = {"error": "New Password is too short. Try another"}
			elif not upper_case:
				response = {"error": "New Password must contain at least one Uppercase."}
			elif not digits:
				response = {"error": "New Password must contain at least one number."}
			elif not chars:
				response = {"error": "New Password must contain at least one character."}
			else:

				# password = make_password(new_password)
				user.set_password(new_password1)
				user.save()
				response = {"success": "Password successfully changed."}
			return JsonResponse(response)
		else:
			response = {"error": "We could not understand your request."}
			return JsonResponse(response)
	else:
		response = {"error": "Sorry. We could not process your request. Try again."}
		return JsonResponse(response)

@login_required
def change_password(request):
	return render (request, 'change_password.html')



def dashboard (request):
	user_wallet = UserWallet.objects.get(user=request.user)
	pay_history = PayHistory.objects.filter(user=request.user).order_by('id').reverse()[:4]
	context = {
		'user_wallet': user_wallet.amount,
		'prev_amt': user_wallet.prev_amount,
		'pay_history': pay_history
	}
	return render (request, 'dashboard.html', context)


def service(request):
	return render(request, 'service.html')

def data_service(request):
	return render (request, 'datas.html')

def data_purchase(request):
	if request.is_ajax():
		user = request.user
		network = request.POST.get("network", None)
		mobile = request.POST.get("mobile", None)
		amount = request.POST.get("amount", None)
		data_plan = request.POST.get("data_plan", None)
		wallet = UserWallet.objects.get(user=request.user)
		
		if Decimal(amount) > wallet.amount:
			response = {'error': 'You do not have have sufficient fund in your wallet.'}
			return JsonResponse(response)
		url = 'https://www.alexdata.com.ng/api/data/'
		headers = {
			"Authorization": "Token " +settings.ALEX_DATA_KEY,
			'Content-Type': 'application/json'
		}
		datum = {
			"network": network,
			"mobile_number": mobile,
			"plan": data_plan
		}
		x = requests.post(url, data=json.dumps(datum), headers=headers)
		ref_code = 'REFNO'+secrets.token_hex(7)

		user_wallet = UserWallet.objects.get(user=user)
		current_amount = user_wallet.prev_amount
		
		# results = x.json()['success']
		if x.status_code == 500:
			PayHistory.objects.create(
				user=user, purpose="airtime", paystack_charge_id=ref_code, prev_amount=current_amount, amount=amount, paid=False, status=False
			)
			response = {'error': "Error500: Internal Server Error"}
			status = 'error'
		elif 'detail' in x.json():
			PayHistory.objects.create(
				user=user, purpose="airtime", paystack_charge_id=ref_code, prev_amount=current_amount, amount=amount, paid=False, status=True
			)
			response = {'error': x.json()}
			status = 'error'
		elif 'error' in x.json():
			PayHistory.objects.create(
				user=user, purpose="airtime", paystack_charge_id=ref_code, prev_amount=current_amount, amount=amount, paid=False, status=False
			)
			response = {'error': x.json()['error']}
			status = 'error'
		else:
			PayHistory.objects.create(
				user=user, purpose="airtime", paystack_charge_id=ref_code, prev_amount=current_amount, amount=amount, paid=True, status=True
			)
			response = {'success': x.json()['success']}
			status = 'success'
		# data_history = DataHistory.objects.create(user=request.user, amount="300", status=status, network=network, plan=data_plan, mobile_number=mobile, transaction_id=ref_code)
		# data_history.save()
		# if (status == 'success'):
			user_wallet = UserWallet.objects.get(user=request.user)
			user_wallet.amount -= Decimal(amount)
			user_wallet.save()
		data_history = DataHistory.objects.create(user=request.user, amount=amount, status=status, network=network, plan=data_plan, mobile_number=mobile, transaction_id=ref_code)
		data_history.save()

		return JsonResponse(response)

def airtime_service(request):
	return render(request, 'airtimes.html')

def airtime_purchase(request):
	if request.is_ajax():
		user = request.user
		network = request.POST.get("network", None)
		mobile = request.POST.get("mobile", None)
		amount = request.POST.get("amount", None)
		wallet = UserWallet.objects.get(user=request.user)
		if Decimal(amount) > wallet.amount:
			response = {'error': 'You do not have have sufficient fund in your wallet.'}
			return JsonResponse(response)
		url = 'https://www.alexdata.com.ng/api/topup/'
		headers = {
			"Authorization": "Token " +settings.ALEX_DATA_KEY,
			'Content-Type': 'application/json'
		}
		datum = {
			"network": network,
			"mobile_number": mobile,
			"amount": amount
		}
		x = requests.post(url, headers=headers, data=json.dumps(datum))
		ref_code = 'REFNO'+secrets.token_hex(7)
		user_wallet = UserWallet.objects.get(user=user)
		current_amount = user_wallet.prev_amount
		
		# results = x.json()['success']
		if 'error' in x.json():
			PayHistory.objects.create(
				user=user, purpose="airtime", paystack_charge_id=ref_code, prev_amount=current_amount, amount=amount, paid=False, status=False
			)
			response = {'error': x.json()['error']}
			status = "error"
		else:
			PayHistory.objects.create(
				user=user, purpose="airtime", paystack_charge_id=x.json()['id'], prev_amount=current_amount, amount=amount, paid=True, status=True
			)
			response = {'good': 'You have successfully recharged '+x.json()['mobile_number']}
			status = "success"
			user_wallet = UserWallet.objects.get(user=request.user)
			user_wallet.amount -= Decimal(amount)
			user_wallet.save()
		airtime_history = AirtimeHistory.objects.create(user=request.user, prev_amount=current_amount, amount=amount, status=status, network=network, mobile_number=mobile, transaction_id=x.json()['id'])
		# airtime_history.save()
		return JsonResponse(response)

def services (request):
	return render (request, 'services.html')

def wallet (request):
	return render (request, 'wallet.html')

def data (request):
	return render (request, 'data.html')

def cable (request):
	return render (request, 'cable.html')

def airtime (request):
	return render (request, 'airtime.html')

def electricity (request):
	return render (request, 'electricity.html')

def profile (request):
	return render (request, 'profile.html')

def funding (request):
	context = {
		'paystack_key': settings.PAYSTACK_PUBLIC_KEY
	}
	# print(context)
	return render (request, 'funding.html', context)


def create_wallet_history(request):
	if request.is_ajax():
		user = request.user
		PayHistory.objects.create(user=user, purpose="wallet", paystack_charge_id=request.POST["reference"], amount=request.POST['amount'], paid=False, status=False)
		return JsonResponse("success")


class Verify_Payment(APIView):
	def get(self, request):
		user = request.user
		user_wallet = UserWallet.objects.get(user=user)
		prev_amt = user_wallet.amount
		# user_wallet.prev_amount = prev_amt
		# user_wallet.save()
		reference = request.GET.get("reference")
		url = 'https://api.paystack.co/transaction/verify/'+reference
		headers = {
			"Authorization": "Bearer " +settings.PAYSTACK_SECRET_KEY
		}
		x = requests.get(url, headers=headers)
		if x.json()['status'] == False:
			return False
		results = x.json()
		if results['data']['status'] == 'success':
			amt= results["data"]["amount"]/100
			user_wallet.prev_amount = prev_amt
			user_wallet.save()
			PayHistory.objects.create(
				user=user, purpose="wallet",
				paystack_charge_id=results["data"]["reference"],
				amount=amt, prev_amt=prev_amt, post_amt=user_wallet, paid=True, status=True
			)
		else:
			user_wallet.prev_amount = prev_amt
			user_wallet.save()
			amt= results["data"]["amount"]/100
			PayHistory.objects.create(
				user=user, purpose="wallet",
				paystack_charge_id=results["data"]["reference"],
				amount=amt, prev_amt=prev_amt, post_amt=user_wallet, paid=True, status=False
			)
		current_wallet = UserWallet.objects.get(user=user)
		current_wallet.amount += (results["data"]["amount"] /Decimal(100))
		current_wallet.save()

		return Response(results)


def contactus(request):
	return render(request, 'contact-us.html')

def contact(request):
	if request.is_ajax():
		name = request.POST.get('name', None)
		email = request.POST.get('email', None)
		phone = request.POST.get('mobile', None)
		subject = request.POST.get('subject', None)
		message= request.POST.get('message', None)

		site_name = settings.SITE_NAME

		# Let's setup variable's to add to our template
		subject_file = os.path.join(settings.BASE_DIR, "mail/contact/subject.txt")
		subject_1 = render_to_string(subject_file, {'name': name, 'site_name': site_name})
		from_email = email
		to_email = [settings.DEFAULT_EMAIL_SENDER]

		contact_message_file = os.path.join(settings.BASE_DIR, "mail/contact/body.txt")
		contact_message = render_to_string(contact_message_file, {
													'name': name, 'email': email,
													'phone': phone, 'subject': subject, 'message': message, 'site_name': site_name,
												})

		message_1 = EmailMultiAlternatives(subject=subject_1, body=contact_message, from_email=from_email, to=to_email)

		html_template = os.path.join(settings.BASE_DIR, "mail/contact/body.html")
		template = render_to_string(html_template, {
													'name': name, 'email': email,
													'phone': phone, 'subject': subject, 'message': message, 'site_name': site_name,
													})

		message_1.attach_alternative(template, "text/html")

		message_1.send()
		if message.send():

			# contactinfo = Contactinfo(name=name,email=email,phone=phone,subject=subject,message=message)
			# contactinfo.save()
			response = {"success": "Your message has been sent successfully, we will get back to you soon!"}
		else:
			response = {"error": "Sorry, try again please."}
		return JsonResponse(response)

# def webhook (request):
# 	return render (request, 'webhook.html')

def transactionhistory (request):
	pay_history = PayHistory.objects.filter(user=request.user).order_by('id').reverse()
	user_wallet = UserWallet.objects.get(user=request.user)
	context = {
		'pay_history': pay_history,
		'user_wallet': user_wallet.amount,
		'prev_amt': user_wallet.prev_amount
		# 'user_wallet': user_wallet
	}
	return render (request, 'transactionhistory.html', context)

def webhook (request):
	if request.method == 'POST':
		email = request.POST['email']
		amount = request.POST['payamount']
		firstname = request.user.first_name
		lastname = request.user.last_name
		amount = int(amount)*100

		# print(email)print(firstname)print(lastname)print(amount)
		initialized = init_payment(firstname, lastname, email, amount)
		print(initialized["data"]["authorization_url"])
		amount = amount/100
		instance = PayHistory.objects.create(amount=amount, user=request.user, paystack_charge_id=initialized['data']['reference'], paystack_access_code=initialized['data']['access_code'])

		wallet = UserWallet.objects.get(user=request.user)
		old_amt = wallet + amount
		wallet.save()
		
		link = initialized['data']['authorization_url']
		return HttpResponseRedirect(link)
	return render (request, 'webhook.html')


# def get_cable_plan(request):
# 	if request.is_ajax():
# 		result = fetch_cable_plan()
# 		print(result)
# 		response = {"success": "yeah"}
# 		return JsonResponse(response)

def cable_service(request):
	return render (request, 'cables.html')

def cable_purchase(request):
	if request.is_ajax():
		network = request.POST.get("network", None)
		mobile = request.POST.get("mobile", None)
		amount = request.POST.get("amount", None)
		cable_plan = request.POST.get("cable_plan", None)
		wallet = UserWallet.objects.get(user=request.user)
		if Decimal(amount) > wallet.amount:
			response = {'error': 'You do not have have sufficient fund in your wallet.'}
			return JsonResponse(response)
		url = 'https://www.alexdata.com.ng/api/topup/'
		# url = 'https://www.alexdata.com.ng/api/topup/'
		headers = {
			"Authorization": "Token " +settings.ALEX_DATA_KEY,
			'Content-Type': 'application/json'
		}
		datum = {
			"network": network,
			"mobile_number": mobile,
			"plan": cable_plan
		}
		x = requests.post(url, headers=headers, data=json.dumps(datum))
		# print(x.json())
		
		# results = x.json()['success']
		if x.status_code == 500:
			response = {'error': "Error500: Internal Server Error"}
		elif x.json()['detail']:
			response = {'error': x.json()['detail']}
		elif x.json()['error']:
			response = {'error': x.json()['error']}
		else:
			response = {'success': x.json()['success']}
			user_wallet = UserWallet.objects.get(user=request.user)
			user_wallet.amount -= Decimal(amount)
			user_wallet.save()
		return JsonResponse(response)



def get_electricity_plan(request):
	if request.is_ajax():
		result = fetch_electricity_plan()
		print(result)
		response = {"success": "yeah"}
		return JsonResponse(response)

def electricity_service(request):
	return render (request, 'electricitys.html')

def electricity_purchase(request):
	if request.is_ajax():
		network = request.POST.get("network", None)
		mobile = request.POST.get("mobile", None)
		amount = request.POST.get("amount", None)
		plan_type = request.POST.get("plan_type", None)
		wallet = UserWallet.objects.get(user=request.user)
		if Decimal(amount) > wallet.amount:
			response = {'error': 'You do not have have sufficient fund in your wallet.'}
			return JsonResponse(response)
		url = 'https://ringo/public/ringoPayments/public/api/test/b2b/'
		# url = 'https://www.alexdata.com.ng/api/topup/'
		headers = {
			# "Authorization": "Token " +settings.ALEX_DATA_KEY,
			# 'Host': 34.74.220.10
			'email': 'member@mail.com',
			'password': '12345678',
			'Content-Type': 'application/json'
		}
		datum = {
			"serviceCode": "P-ELECT",
			"disco": network,
			"meterNo": mobile,
			"type": plan_type,
			"amount": amount,
			"phonenumber": "08118236545",
			"request_id": "23213335433"
		}
		x = requests.post(url, headers=headers, data=json.dumps(datum))
		# print(x.json())
		
		# results = x.json()['success']
		if x.status_code == 500:
			response = {'error': "Error500: Internal Server Error"}
		elif x.json()['detail']:
			response = {'error': x.json()['detail']}
		elif x.json()['error']:
			response = {'error': x.json()['error']}
		else:
			response = {'success': x.json()['success']}
			user_wallet = UserWallet.objects.get(user=request.user)
			user_wallet.amount -= Decimal(amount)
			user_wallet.save()
		return JsonResponse(response)

def NewNotification(request):
	return render(request, 'create-notification.html')

def Notify(request):
	if request.is_ajax():
		title = request.POST.get("title")
		message = request.POST.get("message")
		featured = request.POST.get("featured")
		users = User.objects.all()

		instance = Notification.objects.create(title=title, message=message, is_featured=featured)
		for user in users:
			UserNotification.objects.create(user=user, message=instance)

		response = {"success": "Notification Created Successfully"}
	else:
		response = {"error": "Error. Try Again."}

	return JsonResponse(response)

def manualfunding(request):
	return render (request, 'manual_funding.html')

def all_notifications(request):
	notification = UserNotification.objects.filter(user=request.user)
	context = {
		'notification': notification
	}
	return render(request, 'notifications.html', context)


def single_notification(request, pk):
	notification = UserNotification.objects.get(pk=pk)
	notification.read = True
	notification.save()
	context = {
		'notification': notification
	}
	return render(request, 'read-notification.html', context)


def gen_ussd(request):
	if request.is_ajax():
		bank = request.POST.get("bank", None)
		amount = request.POST.get("amount", None)
		email = request.user.email
		tx_ref = gen_ref()
		fullname = request.user.first_name + ' ' + request.user.last_name
		phone_number = request.user.mobile

		url = 'https://api.flutterwave.com/v3/charges?type=ussd'
		headers = {
			"Authorization": "Bearer "+settings.FLUTTERWAVE_SECRET_KEY,
			"Content-Type": "application/json"
		}
		payload = {
			"tx_ref": "AH"+tx_ref,
			"email": email,
			"amount": amount,
			"account_bank": bank,
			"currency": "NGN",
			"phone_number": phone_number,
			"fullname": fullname,
		}
		x = requests.post(url, data=json.dumps(payload), headers=headers)
		if x.json()['status'] != "success":
			return False
		results = x.json()
		response = {"message": results["message"], "ussd_code": results["meta"]["authorization"]["note"]}
		return JsonResponse(response)

def manual_funding (request):
	return render (request, 'manual_funding.html')
