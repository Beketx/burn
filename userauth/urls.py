from django.urls import re_path, include,path

from .views import RegistrationClientAPIView, RegistrationDeveloperAPIView
from .views import LoginAPIView, Test, ValidateOTP, ValidatePhoneSendOTP

urlpatterns = [
    re_path(r'^registration/client/?$', RegistrationClientAPIView.as_view(), name='user_registration'),
    re_path(r'^registration/developer/?$', RegistrationDeveloperAPIView.as_view(), name='user_registration'),
    re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),
    path('test/', Test.as_view()),
    path('send-otp/', ValidatePhoneSendOTP.as_view()),
    path('validate-otp/', ValidateOTP.as_view())
]