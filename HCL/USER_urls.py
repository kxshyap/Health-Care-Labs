from django.db import models
from django.urls import path,include
from HCL import USER_views

# Create your models here.

urlpatterns = [
    path('',USER_views.index),
    path('user_account/',USER_views.user_account,name='user_account'),
    path('userlogout/',USER_views.userlogout),
    path('about/',USER_views.about),
    path('pricing/',USER_views.pricing),
    path('contact/',USER_views.contact),
    path('test_booking/',USER_views.test_booking),
    path('forget_password/',USER_views.forget_password),
    path('updateprofile/',USER_views.updateprofile),

]