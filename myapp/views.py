from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.core.mail import send_mail
from FinalProject import settings
import random
import requests

status=False
def index(request):
    global status
    if request.method=='POST':
        if request.POST.get('signup')=='signup':
            newuser=signupForm(request.POST)
            if newuser.is_valid():
                newuser.save()
                print("Signup Successfully!")
            else:
                print(newuser.errors)
        elif request.POST.get('login')=='login':

            unm=request.POST['username']
            pas=request.POST['password']

            user=signupmaster.objects.filter(username=unm,password=pas)
            uid=signupmaster.objects.get(username=unm)
            print("UserID:",uid.id)
            if user:
                print("Login Successfully!")
                request.session['user']=unm
                request.session['uid']=uid.id
                #msg="Login Successfully!"
                status=True
                return redirect('notes')
            else:
                print("Error!Login Fail...Try again")
    return render(request,'index.html')

def notes(request):
    #global status
    user=request.session.get('user')
    if request.method=='POST':
        newnotes=notesForm(request.POST, request.FILES)
        if newnotes.is_valid():
            newnotes.save()
            print("Signup Successfully!")
        else:
            print(newnotes.errors)
    return render(request,'notes.html',{'user':user})

def profile(request):
    user=request.session.get('user')
    uid=request.session.get('uid')
    cuser=signupmaster.objects.get(id=uid)
    if request.method=='POST':
        newuser=updateForm(request.POST,instance=cuser)
        if newuser.is_valid():
            newuser.save()
            print("Profile updated!")
            return redirect("notes")
        else:
            print(newuser.errors)
    return render(request,'profile.html',{'user':user,'cuser':cuser})

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=='POST':
        newfeedback=feedbackForm(request.POST)
        if newfeedback.is_valid():
            newfeedback.save()
            print("Your feedback has been submitted!")

            #Email Send
            otp=random.randint(1111,9999)
            sub="Thank you!"
            msg=f"Hello {request.POST['name']}!\n\nWe have received your feedback.\nWe will contact you in shortly.\n\nIf any queries regarding, contact us anytime on\n\n +91 9724799469 | sanket.tops@gmail.com\n\nThanks & Regards!\nTOPS Technologies Pvt Ltd - Rajkot\nYour OTP is:{otp}\n 972479949 | help@tops-int.com | www.tops-int.com"            
            from_mail=settings.EMAIL_HOST_USER
            to_mail=['dhrutidharkotadiya51@gmail.com','djangotestingpython@gmail.com']
            #to_mail=[request.POST['email']]

            send_mail(subject=sub,message=msg,from_email=from_mail,recipient_list=to_mail)


            #OTP Sending
            url = "https://www.fast2sms.com/dev/bulkV2"
            #querystring = {"authorization":"KEodGZf5On3eCxJPkWAFHQUYtS86Rbmrv1MyuViag4hs7N2DujvzKSw5MN9mRryb3LC4DsIHiWph78","variables_values":f"{otp}","route":"otp","numbers":f"{request.POST['mob']}"}

            querystring = {"authorization":"KEodGZf5cn3eCxJPkWAFHQUYtS86Rbmrv1MyuViag4hs7N2DujvzKSw5MN9mRryb3LC4DsIHiWph78","message":f"Dear User\nGood Morning from TOPS Technologies\nvisit:www.tops-int.com","language":"english","route":"q","numbers":"9586632371,6352789893,8239430873"}
            headers = {
                'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
        else:
            print(newfeedback.errors)
    return render(request,'contact.html')

def userlogout(request):
    logout(request)
    return redirect('/')