from django.db import models
from datetime import datetime
from django.contrib.auth.hashers import make_password

class user_info(models.Model):
    created=models.DateTimeField(default=datetime.now(),blank=True)
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    uname=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    zip=models.IntegerField()
    mobile=models.BigIntegerField()

class test_info(models.Model):
    created=models.DateTimeField(default=datetime.now(),blank=True)
    testname=models.CharField(max_length=150)
    test_date=models.DateField()
    test_time=models.CharField(max_length=20)
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.EmailField()
    mobile=models.BigIntegerField()
    gender=models.CharField(max_length=50)
    age=models.IntegerField()
    verification_doc=models.FileField(upload_to='Verification Documents')
    address=models.TextField()
    test_price=models.IntegerField()
    mop=models.CharField(max_length=100) # mop = mode of payment
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    status=models.CharField(blank=True,max_length=20, choices=STATUS_CHOICES, default='pending')

class contact_info(models.Model):
    created=models.DateTimeField(default=datetime.now(),blank=True)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    comments=models.TextField()
