from django.shortcuts import render
from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone
from .send_mail import sendmail
import uuid
from .models import ForgetTokenManager

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST['number']     #number as username
        email = request.POST['email'] 
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        # Check inputs:


        # checking passwords
        if str(password1) != str(password2) :
            return JsonResponse({'error': 'Passwords doesnot match'})
        
        if len(password1) < 8 or len(password2) < 8:
            return JsonResponse({'error': 'Password must be at least 8 characters'})
        
        # checking number
        if len(username) !=10:
            return JsonResponse({'error': 'must be 10 digit number'})

        
        # creating user
        # import User
        try:
            # check if email is already taken
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'email already taken'})  
            
            users = User.objects.create_user(username,email, password1)
            users.first_name = fname.lower()
            users.last_name = lname.lower()
            users.last_login =timezone.now()
            users.save()
            return JsonResponse({'success': 'user created'})
        
        except Exception as e:
            return JsonResponse({'error': 'Number is already registered'})
  
    return JsonResponse({'error': 'only post is available'})

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        # data from frontend
        username = request.POST['emailorphone']
        password = request.POST['password']
        print(password)

        # authentications:
        user=None
        if '@' in username:
            try:
                user = authenticate(username=User.objects.get(email=username), password=password)
            except:
                return JsonResponse("error:Invalid Login from email")
        else:
            try:
                user = authenticate(username=User.objects.get(username=username), password=password)    
            except:
                return JsonResponse("error:Invalid Login from number")

    
        if user is not None:
            login(request, user)
            return JsonResponse({'success': 'success Login'})

        else:
            return JsonResponse({'error':'Cant login try again'})
            
    return JsonResponse({'error': 'only post is available'})

@login_required
@csrf_exempt
def signout(request):
    logout(request)
    return JsonResponse({'success':'logout successfull'})


# handle forget password
@csrf_exempt
def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        # check if email exists
        if not User.objects.filter(email=email).exists():   #since email is unique we can use filter
            return JsonResponse({'error': 'email not exists'})
        
        try:
            #send email to existing email with unique uuid
            uid=str(uuid.uuid4())
            
            #  save token

            user_obj=User.objects.get(email=email)
            token_obj,created=ForgetTokenManager.objects.get_or_create(user=user_obj)
         
            # even token is already created we simply just update it
            token_obj.forget_password_token=uid
            # print(token_obj.forget_password_token)

            token_obj.save()
            # send mail
            sended=sendmail(email,uid)
            # print("sent:",sended)
         
            if not sended:
                return JsonResponse({'error':"Cant able to send the mail"})

            return JsonResponse({'success':"Successfully sent the mail"})

        except Exception as e:
            return JsonResponse({'error':'some error occured'})
        
    return JsonResponse({'error': 'only post is available'})

# used for resetting password
@csrf_exempt
def resetPassword(request,token):
    if request.method=="POST":
        
        try:
            # return the user with token saved
            forgetTokenManager_obj=ForgetTokenManager.objects.get(forget_password_token=token)
            # print(forgetTokenManager_obj.user)
            
            # data from front
            password1=request.POST['password1']
            password2=request.POST['password2']

            # check passwords
            if str(password1) != str(password2) :
                return JsonResponse({'error': 'Passwords doesnot match'})
                
            if len(password1) < 8 or len(password2) < 8:
                return JsonResponse({'error': 'Password must be at least 8 characters'})
            
            # set new password
            try:
                user=forgetTokenManager_obj.user
                user.set_password(password1)
                user.save()
                return JsonResponse({'success': 'sucessfully reset password'})
                
            except Exception as e:
                return JsonResponse({'error': 'unable to reset password'})

        except Exception as e:
            return JsonResponse({'error': "Some error occured"})
        
    return JsonResponse({'error': 'only post is available'})