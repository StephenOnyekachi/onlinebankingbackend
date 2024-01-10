from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Gender(models.Model):
    gender = models.CharField(max_length=100)
    def __str__(self):
        return self.gender

class Bank(models.Model):
    bank = models.CharField(max_length=200)
    def __str__(self):
        return self.bank

class Currency(models.Model):
    currency = models.CharField(max_length=100)
    def __str__(self):
        return self.currency

class Account_type(models.Model):
    account_type = models.CharField(max_length=100)
    def __str__(self):
        return self.account_type


SUCCESS = "success"
FAILD = "faild"

STATUS = [ 
    (SUCCESS,"Success"),
    (FAILD,"Faild")
]

@receiver(post_save, sender=User)
def create_auth_token(sender, instance= None, created=False, **kwargs):
    if created:
        Users.objects.create(user=instance)

class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=200)
    address = models.CharField(max_length=250)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    balance = models.FloatField(default=0.00, null=True)
    account_number = models.PositiveIntegerField(default=0, null=True)
    account_type = models.CharField(max_length=200)
    bank = models.CharField(max_length=200)
    block = models.BooleanField(default=False)
    gender = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
    
    
class OTP(models.Model):
    otp = models.PositiveIntegerField()
    sent_time = models.DateTimeField(verbose_name="sent time", auto_now=True)
    expired_time = models.DateTimeField(verbose_name="expired time", auto_now=True)

    def __str__(self):
        return self.otp

class Transactions(models.Model):
    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='receiver')
    amount = models.PositiveIntegerField(default=0.00)
    time_stamp = models.DateTimeField(verbose_name="time stamp", auto_now=True)
    otp = models.PositiveIntegerField()
    reffrence_code = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    def __int__(self):
        return self.amount
