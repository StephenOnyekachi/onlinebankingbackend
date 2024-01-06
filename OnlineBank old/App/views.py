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
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm 
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# Create your views here.

# def password_reset_request(request):
#     if request.method == 'POST':
#         password_form = PasswordResetForm(request.POST)
#         if password_form.is_valid():
#             data = password_form.cleaned_data['email']
#             user_email = Users.objects.filter(Q(email=data))
#             if user_email.exists():
#                 for user in user_email:
#                     subject = 'Password Request'
#                     email_template_name = 'nav_auth/password_message.txt'
#                     parameters = {
#                         'email' : user.email,
#                         'domain' : 'https://127.0.0.1:8000',
#                         'site_name' : 'onlinebank',
#                         'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
#                         'token' : default_token_generator.make_token(user),
#                         'protocol' : 'https',
#                     }
#                     email = render_to_string(
#                         email_template_name,
#                         parameters
#                     )
#                     try:
#                         send_mail(
#                             subject,
#                             email,
#                             '',
#                             [user.email],
#                             fail_silently=False,
#                         )
#                     except:
#                         return HttpResponse('Invalid Header')
#                     return redirect('password_reset_done')
#     else:
#         password_form = PasswordResetForm()
#     context = {
#         'password_form':password_form,
#     }
#     return render(request, 'nav_auth/reset_password.html', context)

def Create_new_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        last_name = request.POST['lastname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if Users.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            else:
                Users.objects.create_user(
                    username = username,
                    first_name = first_name,
                    last_name = last_name,
                    phone_number = phone_number,
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
    user = request.user
    all_history = Transactions.objects.all().order_by('-id')
    sender_history = Transactions.objects.filter(sender=user).order_by('-id')
    receiver_history = Transactions.objects.filter(receiver=user).order_by('-id')

    context = {
        'user':user,
        'all_history':all_history,
        'sender_history':sender_history,
        'receiver_history':receiver_history,
    }
    return render(request, 'profile/dashboard.html', context)

def All_users(request):
    users = Users.objects.filter(is_superuser=False).order_by('-id')
    context = {
        'users':users,
    }
    return render(request, 'profile/all_users.html', context)

def View_profile(request):
    user = Users.objects.get(username=request.user)
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        user.profile_picture = profile_picture
        user.save()
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
        messages.info(request, f'you just unblock {user.username}')
        return redirect('dashboard')
    user.block = True
    user.save()
    messages.info(request, f'you just block {user.username}')
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
        profile_picture = request.FILES.get('profile_picture')
        
        user.currency = currency
        user.account_type =account_type
        user.bank = bank
        user.gender = gender
        user.country = country
        user.address = address
        user.balance = balance
        user.profile_picture = profile_picture
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

# def Otp(request):
#     otp = str(random.randint(1000, 9999))
#     while len(OTP.objects.filter(otp=otp)) != 0:
#         otp = str(random.randint(1000, 9999))
#         print('otp is',otp)
#         messages.success(request, f'{otp}')

#     OTP.objects.create(
#         otp=otp,
#     )
    # return redirect('transfer_finish')

def Transfer(request):
    user = request.user
    
    otp = str(random.randint(100000, 999999))
    while len(Transfer_otp.objects.filter(otp_code =otp)) != 0:
        otp = str(random.randint(1000, 9999))
        print('otp is',otp)
        messages.success(request, f'{otp}')

    Transfer_otp.objects.create(
        user = user,
        otp_code=otp,
    )

    context = {
        'user': user,
    }
    return render(request, 'profile/trasfer.html', context)

def Transfer_finish(request):

    if request.method == 'GET':
        amount = request.GET['amount']
        account = request.GET['account_number']
        receiver = Users.objects.get(account_number=account)

    if request.method == 'POST':
        amount = request.POST['amount']
        account = request.POST['account_number']
        receiver = Users.objects.get(account_number=account)

        user = request.user

        otp = request.POST.get('otp')

        if Transfer_otp.objects.filter(user=user, otp_code=otp).exists():

            # context = {
            #     'amount':amount,
            #     'account':account,
            #     'receiver':receiver,

            #     'otp':otp,
            # }
            
            return redirect('confirm')
        else:
            print('falied')

    context = {
        'amount':amount,
        'account':account,
        'receiver':receiver,
    }
    return render(request, 'profile/trasfer_finish.html', context)

def Confirm(request):
    
    uni = 'acxr'
    rand1 = str(random.randint(100, 999))
    ref_code = uni + rand1
    while len(Transactions.objects.filter(reffrence_code=ref_code)) != 0:
        rand1 = str(random.randint(1000, 9990))
        ref_code = uni + rand1

    if request.method == 'GET':
        amount = request.GET['amount']
        account = request.GET['account_number']
        receiver = Users.objects.get(account_number=account)

        otp = request.GET('otp')

    if request.method == 'POST':
        account = request.POST.get('account_number')
        print(account)
        amount = request.POST['amount']
        otp = request.POST['otp']

        receiver = Users.objects.get(account_number=account)

        # receiver = Users.objects.get(account_number=account)
        sender = Users.objects.get(username=request.user)
        
        set_amount = sender.balance

        if set_amount < int(amount):
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
                otp = otp,
            )

            delete_otp = Transfer_otp.objects.get(user=request.user)
            if delete_otp:
                delete_otp.delete()

            messages.info(request, 'Transactions Success')
            return redirect('dashboard')
        
    context = {
        'amount':amount,
        'account':account,
        'receiver':receiver,

        'otp':otp,
    }
        
    return render(request, 'profile/confirm.html', context)

def History(request, pk):
    history = Transactions.objects.get(id=pk)
    context = {
        'history':history,
    }
    return render(request, 'profile/history.html', context)

