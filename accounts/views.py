from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
import math, random

#Login User
def login1(request):
    previous=request.META.get('HTTP_REFERER')
    nextt=request.GET.get('next',None)
    if nextt:
        nextt=nextt[1:-1]
    context={"previous":previous,"next":nextt}
    if request.method== 'POST':
        previous=request.POST.get('previous')
        next=request.POST.get('next')
        email=request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        user_obj=User.objects.filter(username=username).first()
        profile_obj=profile_obj = Profile.objects.filter(user=user_obj).first()
        if user_obj is None:
            messages.info(request,'User Not found')
            return redirect('login1')
        
        if not profile_obj.is_verified:
            messages.info(request,'Email not verified yet')
            u=User.objects.get(username=username)
            prof=Profile.objects.get(user=u)
            auth_token=prof.auth_tokens
            send_mail_later(email,auth_token)
            return redirect("token_sent")

        if user is not None:
            auth.login(request,user)
            messages.info(request,'Logged in Successfully')
            if next != 'None':
                return redirect(next)
            elif previous != 'None':
                return redirect(previous)
            else:
                return redirect('/')
        else:
            messages.info(request,'Check your Credentials')
            return redirect('account/login1')
    else:
        return render(request,'accounts/login1.html',context)    


#Register User for creating ac
def register(request):
    if is_ajax(request=request):
        otp=generateOTP()
        if request.POST.get("form")=="otp":
            email_ajax=request.POST.get("email")
            htmlgen = f'Dear User, <br> Please Enter below <strong>OTP</strong> to create your NepTravelBlog account <br><h2>Your OTP is <strong>{otp}</strong></h2>'
            try:
                send_mail('Verification for NepTravelBlog Account',f'{otp}',settings.EMAIL_HOST_USER,[email_ajax], fail_silently=False, html_message=htmlgen)
                response={'otp_sent':otp,'msg':'OTP Sent Successfully!'}
            except:
                response={'otp_sent':'','msg':'Error'}
            return JsonResponse(response)
        response={'otp_sent':'','msg':'Error'}
        return JsonResponse(response)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:   
                user_obj = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name,last_name=last_name)
                user_obj.save()
                auth_token=str(uuid.uuid4())
                profile_obj=Profile.objects.create(user=user_obj,auth_tokens=auth_token)
                profile_obj.save()
                send_mail_later(email,auth_token)
                return redirect('token_sent')
        else:
            messages.info(request,'password not matching..')    
            return redirect('register') 
    else:
        return render(request,'accounts/register1.html')


#Logout User
def logout(request):
    auth.logout(request)
    return redirect('login1')

#Token sent in gmail
def token_sent(request):
    return render(request,'accounts/tokensent.html')


#User profile verification
def verify(request , auth_tokens):
    profile_obj = Profile.objects.filter(auth_tokens = auth_tokens).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request, 'Your account is already verified.')
            return redirect('login1')

        else:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login1')
    else:
        return redirect('register')
        
#send mail
def send_mail_later(email,token):
    subject='Your account need to be verified'
    message=f'Hi, Paste the link to verify your account http://127.0.0.1:8000/accounts/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(6) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP