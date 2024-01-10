import random
from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import random
from .models import *

# for emails 
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm 
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# Create your views here.

def Index(request):
    if request.method == 'POST':
        message = request.POST['message']
        email = request.POST['email']
        name = request.POST['name']
        send_mail(
            subject = name,
            message = message,
            recipient_list = [email],
            from_email = None,
            fail_silently=False
        )
    context = {
        # 'cart':cart,
    }
    return render(request, 'index.html', context)


def password_reset_request(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Password Request'
                    email_template_name = 'nav_auth/password_message.txt'
                    parameters = {
                        'email' : user.email,
                        'domain' : 'https://127.0.0.1:8000',
                        'site_name' : 'onlinebank',
                        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                        'token' : default_token_generator.make_token(user),
                        'protocol' : 'https',
                    }
                    email = render_to_string(
                        email_template_name,
                        parameters
                    )
                    try:
                        send_mail(
                            subject,
                            email,
                            '',
                            [user.email],
                            fail_silently=False,
                        )
                    except:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done')
    else:
        password_form = PasswordResetForm()
    context = {
        'password_form':password_form,
    }
    return render(request, 'nav_auth/reset_password.html', context)


def Create_new_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        email = request.POST['email']
        last_name = request.POST['lastname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            else:
                User.objects.create_user(
                    username = username,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    password = password1,
                )     
                messages.success(request, 'User was successfully')
                return redirect('all_users')
        else:
            messages.info(request, 'password not matching...')
            return redirect('newstatff') 
    
    context = {
        
    }
    return render(request, 'nav_auth/create_new_user.html', context)

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('dashboard')
            else:
                login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, 'username or password incorrect')
            return redirect('login')
    context = {
        'message': messages,
    }
    return render(request, 'nav_auth/login.html', context)

def UserLogout(request):
    logout(request)
    return redirect('login')

def Index(request):
    context = {
        # 'cart':cart,
    }
    return render(request, 'index.html', context)

def Dashboard(request):
    user = Users.objects.get(user=request.user)
    history = Transactions.objects.all().order_by('-id')

    context = {
        'user':user,
        'history':history,
    }
    return render(request, 'profile/dashboard.html', context)

def All_users(request):
    users = Users.objects.all().order_by('-id')
    context = {
        'users':users,
    }
    return render(request, 'profile/all_users.html', context)

def View_profile(request):
    user = Users.objects.get(user=request.user)
    context = {
        'user':user
    }
    return render(request, 'profile/view_profile.html', context)

def View_user(request, pk):
    user = Users.objects.get(id=pk)
    if request.method == 'POST':
        balance = request.POST['balance']

        user.balance += float(balance)
        user.save()
        messages.success(request, f'{user.user.username} balance is now {user.balance}')
        return redirect('all_users')
    context = {
        'user':user,
    }
    return render(request, 'profile/view_user.html', context)

def Block_user(request, pk):
    user = Users.objects.get(id=pk)
    if user.block:
        user.block = False
        user.save()
        messages.info(request, f'you just unblock {user.user.username}')
        return redirect('dashboard')
    user.block = True
    user.save()
    messages.info(request, f'you just block {user.user.username}')
    return redirect('dashboard')

def Delete_user(request, pk):
    user = Users.objects.get(id=pk)
    user.delete()
    return redirect('dashboard')

def Complete_user(request, pk):
    user = Users.objects.get(id=pk)
    
    uni = '1100'
    rand1 = str(random.randint(100000, 999999))
    acc_number = uni + rand1
    while len(Users.objects.filter(account_number=acc_number)) != 0:
        rand1 = str(random.randint(100000, 999999))
        acc_number = uni + rand1
        # acc_number = int(acc_number)

    if request.method == 'POST':
        currency = request.POST['currency']
        account_type = request.POST['account_type']
        bank = request.POST['bank']
        gender = request.POST['gender']
        country = request.POST['country']
        address = request.POST['address']
        balance = request.POST['balance']
        
        user.currency = currency
        user.account_type =account_type
        user.bank = bank
        user.gender = gender
        user.country = country
        user.address = address
        user.balance = balance
        try:
            if user.account_number:
                user.account_number=user.account_number
            else:
                user.account_number = acc_number
        except:
            user.account_number=user.account_number     

        user.save()
        return redirect('dashboard')

    context = {
        'user':user,
    }
    return render(request, 'nav_auth/complete_user.html', context)

def Transfer(request):
    user = Users.objects.get(user=request.user)
    context = {
        'user': user,
    }
    return render(request, 'profile/trasfer.html', context)

# user account number == 2215648965

def Transfer_finish(request):

    if request.method == 'GET':
        amount = request.GET['amount']
        account = request.GET['account_number']
        receiver = Users.objects.get(account_number=account)

    # if request.method == 'POST':
    #     otp_code = Transfer_otp.objects.filter(otp=otp_code, user=request.user)
    #     otp = request.POST['otp']
    #     if otp_code is not None:
    #         return redirect('transfer_finish')
    #     else:
    #         return redirect('confirm')


    #     # otp = request.POST['otp']
    #     if otp == otp_code:
    #         return redirect('transfer_finish')
    #     else:
    #         return redirect('confirm')

    context = {
        'amount':amount,
        'receiver':receiver,
    }
    return render(request, 'profile/trasfer_finish.html', context)

def Confirm(request):
    
    uni = 'acxr'
    rand1 = str(random.randint(100, 999))
    ref_code = uni + rand1
    while len(Transactions.objects.filter(reffrence_code=ref_code)) != 0:
        rand1 = str(random.randint(100, 999))
        ref_code = uni + rand1

    if request.method == 'POST':
        account = request.POST.get('account_number')
        print(account)
        amount = request.POST['amount']
        receiver = Users.objects.get(account_number=account)
        sender = Users.objects.get(user=request.user)

        if sender.balance < int(amount):
            messages.info(request, 'insufficient balance try again')
            return redirect('transfer')
        else:
            receiver.balance += int(amount)
            receiver.save()
            sender.balance -= int(amount)
            sender.save()

            receiver_user = receiver
            sender_user = sender

            Transactions.objects.create(
                sender=sender_user, 
                receiver=receiver_user, 
                amount=amount, 
                reffrence_code = ref_code,
                status = 'Success',
                otp = 1234,
            )

            messages.info(request, 'Transactions Success')
            return redirect('dashboard')

def History(request):
    history = Transactions.objects.all().order_by('-id')
    context = {
        'history':history,
    }
    return render(request, 'profile/history.html', context)



def Transfer1(request):

    if request.method == 'POST':
        account = request.POST['account']
        amount = request.POST['amount']
        
        profile = Users.objects.filter(account_number=account) 

        if profile is not None:
            print(profile, account, amount)
            info = [
                profile, account, account
            ]
            messages.success(request, f'{profile}, {account}, {amount}')
            return redirect('pin', info)
        
        else:
            print(account)
            messages.error(request, 'account number not fund')
            return redirect('transfer1')
        
    return render(request, 'transfer.html')

def Transfer_finish1(request):

    if request.method == 'POST':
        pin = request.POST['pin']

        user_pin = Users.objects.get(account_number=pin)
        if user_pin is not None:
            messages.success(request, 'success')
            return redirect('pin')
        else:
            messages.error(request, 'error')
            return(redirect, 'transfer1')
    return render(request, 'pin.html')


def Confirm1(request):
    return render(request, 'confirm.html')

