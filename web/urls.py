from os import name
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.conf import settings
from .views import Verify_Payment

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.index, name='index'),
    url(r'^wallet/$', views.my_wallet, name='wallet'),

    # url(r'^send-confirm-mail/$', views.send_confirm_email_ajax, name='send_confirm_email_ajax'),
    url(r'^confirm-mail/$', views.confirm_email_ajax, name='confirm_email_ajax'),


    ### User Authentication

    url( r'^login/$', views.signin, name="login"),
    url( r'^register/$', views.register, name="register"),
    url(r'^register-ajax/$', views.register_ajax, name='register_ajax'),
    url(r'^signin-ajax/$', views.signin_ajax, name='signin_ajax'),
    url(r'^check-mail-ajax/$', views.check_mail_ajax, name='check_mail_ajax'),
    url(r'^check-username-ajax/$', views.check_username_ajax, name='check_username_ajax'),
    url(r'^check-mobile-ajax/$', views.check_mobile_ajax, name='check_mobile_ajax'),
    url(r'^verify-account/$', views.verifyAccount, name='verify_account'),
    
    # url(r'^send_mail/verification/$', views.send_mail_verification, name='send_mail_verification'),

    re_path(r'^logout/$', auth_views.LogoutView.as_view(),
        {'next_page': settings.LOGIN_REDIRECT_URL}, name='logout'),

    re_path(r'^reset_password/$', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'),
        name='password_reset'),
    url(r'^reset_password_email/$', views.reset_password_email, name='forgot_pass_ajax'),
    url(r'^forgot-password/reset_password/$', views.reset_pass, name='reset_pass'),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
        name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_change.html'),
        name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
        name='password_reset_complete'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^change_password_ajax/$', views.change_password_ajax, name='change_password_ajax'),

    url(r'dashboard', views.dashboard, name='dashboard'),
    url(r'^services/$', views.service, name='service'),
    url(r'^services/airtime/$', views.airtime_service, name='airtimes'),
    url(r'^services/airtime/purchase/$', views.airtime_purchase, name='airtime_purchase'),
    url(r'^services/data/$', views.data_service, name='datas'),
    url(r'^services/data/purchase/$', views.data_purchase, name='data_purchase'),

    url(r'^services/cable/$', views.cable_service, name='cables'),
    url(r'^services/cable/purchase/$', views.cable_purchase, name='cable_purchase'),

    url(r'^services/electricity/$', views.electricity_service, name='electricitys'),
    url(r'^services/electricity/purchase/$', views.electricity_purchase, name='electricity_purchase'),

    url(r'service', views.services, name='services'),
    url(r'contact', views.contact, name='contact'),
    url(r'^reach_us/$', views.contactus, name='reach'),
    # url(r'wallet', views.wallet, name='wallet'),
    url(r'funding', views.funding, name='funding'),
    url(r'^verify_transaction', Verify_Payment.as_view(), name='verify_transaction'),
    url(r'profile', views.profile, name='profile'),
    url(r'transactionhistory', views.transactionhistory, name='transactionhistory'),
    url(r'data', views.data, name='data'),
    url(r'cable', views.cable, name='cable'),
    url(r'airtime', views.airtime, name='airtime'),
    url(r'electricity', views.electricity, name='electricity'),
    url(r'^create_wallet_history/$', views.create_wallet_history, name='create_wallet_history'),
    url(r'webhook', views.webhook, name='webhook'),

    url(r'^ussd-topUp/$', views.manual_funding, name='manual_funding'),
    url(r'^ussd-generate/$', views.gen_ussd, name='gen_ussd'),

    url(r'^notifications/$', views.all_notifications, name='notifications'),
    url(r'^notifications/notify/(?P<pk>[\w.@+-/]+)/$', views.single_notification, name='notification'),
]











