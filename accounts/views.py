from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
import math, random,json

#Login User
def login1(request):
    if is_ajax(request=request):
        otp=generateOTP()
        if request.POST.get("form")=="otp":
            email_ajax=request.POST.get("email")
            htmlgen = f'Dear User, <br> Please Enter below <strong>OTP</strong> to verify your NepTravelBlog account <br><h2>Your OTP is <strong>{otp}</strong></h2>'
            try:
                send_mail('Verification for NepTravelBlog Account',f'{otp}',settings.EMAIL_HOST_USER,[email_ajax], fail_silently=False, html_message=htmlgen)
                response={'otp_sent':otp,'msg':'OTP Sent Successfully!'}
            except:
                response={'otp_sent':'','msg':'Error'}
            return JsonResponse(response)
        elif request.POST.get("form")=="verify":
            username=request.POST.get("username")
            email=request.POST.get("email")
            obj=User.objects.filter(username=username,email=email).first()
            if obj is not None:
                profile_obj=Profile.objects.filter(user=obj).first()
                profile_obj.is_verified=True
                profile_obj.save(update_fields=["is_verified"])
                response={'msg':'','error':''}
                return JsonResponse(response)
                return render(request,'accounts/otp.html',context)
            else:
                response={'msg':'error','error':'Credentials are wrong, could not verify'}
                return JsonResponse(response)
        response={'otp_sent':'','msg':'Error'}
        return JsonResponse(response)
    if request.method== 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        user_obj=User.objects.filter(username=username).first()
        profile_obj = Profile.objects.filter(user=user_obj).first()
        if user_obj is None:
            messages.error(request,'User Not found..')
            return redirect('login1')
        
        if not profile_obj.is_verified:
            context={'username':username,'email':user_obj.email,'verified':'False'}
            return render(request,'accounts/otp.html',context)

        if user is not None:
            auth.login(request,user)
            list(messages.get_messages(request))
            messages.info(request,'Logged in Successfully..')
            return redirect("blog")
        else:
            list(messages.get_messages(request))
            messages.error(request,'Check your Credentials..')
            return redirect("login1")
    else:
        return render(request,'accounts/login1.html')    
    
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
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        otp= request.POST.get('otp')
        sent_otp=request.POST.get('sent_otp')
        country=request.POST.get('country')
        local_body=request.POST.get('local_body')
        bio=request.POST.get('bio')
        profile_image=request.FILES.get('main_img')
        links={"twitter":request.POST.get('twitter',"None"),"instagram":request.POST.get('instagram',"None"),"facebook":request.POST.get('facebook',"None"),"youtube":request.POST.get('youtube',"None")}
        if otp==sent_otp:
            if User.objects.filter(username=username).exists():
                prev_obj=User.objects.get(username=username)
                if Profile.objects.filter(user=prev_obj).first() is not None:    
                    list(messages.get_messages(request))
                    messages.error(request,"Username Taken")
                    return redirect('register')
                else:
                    prev_obj.delete()
                    user_obj = User.objects.create_user(username=username, password=password2, email=email,first_name=first_name,last_name=last_name)
                    user_obj.save()
                    profile_obj=Profile.objects.create(user=user_obj,is_verified=True,country=country,local_address=local_body,bio=bio,profile_img=profile_image,links=json.dumps(links))
                    profile_obj.save()
                    list(messages.get_messages(request))
                    messages.info(request,'User Registeration Successful..')
                    return redirect('login1')
            else:   
                user_obj = User.objects.create_user(username=username, password=password2, email=email,first_name=first_name,last_name=last_name)
                user_obj.save()
                profile_obj=Profile.objects.create(user=user_obj,is_verified=True,country=country,local_address=local_body,bio=bio,profile_img=profile_image,links=json.dumps(links))
                profile_obj.save()
                list(messages.get_messages(request))
                messages.info(request,'User Registeration Successful..')
                return redirect('login1')
        else:
            list(messages.get_messages(request))
            messages.error(request,"OTP Incorrect..") 
            return redirect('register') 
    else:
        return render(request,'accounts/register1.html')

#Profile Update
def profile_update(request,pk):
    context={}
    if request.method=="POST":
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        main_img=request.FILES.get("main_img")
        country=request.POST.get("country")
        local_body=request.POST.get("local_body")
        bio=request.POST.get("bio")
        links={"twitter":request.POST.get('twitter',"None"),"instagram":request.POST.get('instagram',"None"),"facebook":request.POST.get('facebook',"None"),"youtube":request.POST.get('youtube',"None")}
        User.objects.filter(username=pk).update(first_name=fname,last_name=lname)
        Profile.objects.filter(user=request.user).update(country=country,local_address=local_body,bio=bio,links=json.dumps(links))
        if main_img:
            obj=Profile.objects.get(user=request.user)
            prev_pp=obj.profile_img
            obj.profile_img=main_img
            obj.save(update_fields=['profile_img'])
            prev_pp.delete(False)
        messages.info(request,"Profile Updated..")
        return redirect("myblogs", pk=pk)
    if request.user.is_authenticated:
        user_obj=User.objects.filter(username=pk)
        if pk == request.user.username:                
            if len(user_obj)<1:
                messages.error(request,'Profile not found for given username..')
                return redirect("blog")
            else:
                context["user"]=user_obj.first()
                links=json.loads(user_obj.first().profile.links.replace("'", '"'))
                context["links"]=links
                return render(request,'accounts/profile_update.html',context)
        else:
            messages.error(request,"You aren't allowed to visit that page")
            return redirect("myblogs", pk=pk)            
    else:
        messages.error(request,'You must be logged in to visit profiles..')
        return redirect("blog")

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
    message=f'Hi, Paste the link to verify your account https://neptravelblog.pythonanywhere.com/accounts/verify/{token}'
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

def onboarding(request):
    if request.method == "POST":
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        main_img=request.FILES.get("main_img")
        country=request.POST.get("country")
        local_body=request.POST.get("local_body")
        bio=request.POST.get("bio")
        links={"twitter":request.POST.get('twitter',"None"),"instagram":request.POST.get('instagram',"None"),"facebook":request.POST.get('facebook',"None"),"youtube":request.POST.get('youtube',"None")}
        User.objects.filter(username=request.user.username).update(first_name=fname,last_name=lname)
        Profile.objects.create(user=request.user,country=country,local_address=local_body,bio=bio,links=json.dumps(links))
        if main_img:
            obj=Profile.objects.get(user=request.user)
            prev_pp=obj.profile_img
            obj.profile_img=main_img
            obj.save(update_fields=['profile_img'])
            prev_pp.delete(False)
        messages.info(request,"Congratulations! Onboarding complete.")
        return redirect("myblogs", pk=request.user.username)
    return render(request,'accounts/onboarding.html')