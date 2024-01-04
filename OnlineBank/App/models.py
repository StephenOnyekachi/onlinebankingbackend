from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_otp.oath import TOTP
from django_otp.util import random_hex


# Create your models here.

# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance= None, created=False, **kwargs):
#     if created:
#         Users.objects.create(user=instance)

class Users(AbstractUser):
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
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='picture')

    def __str__(self):
        return self.username
    
class Transfer_otp(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_otp')
    otp_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    
# class OTP(models.Model):
#     user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user')
#     otp_code = models.CharField(max_length=6, blank=True, null=True)

#     def generate_otp(self):
#         self.otp_code = random_hex(6)
#         self.save()

#     def verify_otp(self, otp):
#         totp = TOTP(self.otp_code)
#         return totp.verify(otp)

#     # def __int__(self):
#     #     return self.otp_code

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
