from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from hashlib import sha256
from .models import *

from fare.models import *




def hash_with_sha256(password):
    encoded_bytes=password.encode('utf-8')
    password=sha256(encoded_bytes).hexdigest()

@csrf_exempt
def create_bank_account(request):
    if request.method=='POST':
        fullname = request.POST['fullname']
        email = request.POST['email'] 
        phone = request.POST['phone']   
        amount=request.POST['amount']
        nagrita_no=request.POST['nagrita_no']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # check input
        # check if username already exists
        if Bank.objects.filter(email=email).exists() :
            return JsonResponse({'error': 'email already taken'}) 
        if  Bank.objects.filter(phone=phone).exists() :
            return JsonResponse({'error': 'phone already taken'}) 


        # checking passwords
        if str(password1) != str(password2) :
            return JsonResponse({'error': 'Passwords doesnot match'})
        
        if len(password1) < 8 or len(password2) < 8:
            return JsonResponse({'error': 'Password must be at least 8 characters'})

        # check username
        if len(phone) !=10 or not phone.isdigit():
            return JsonResponse({'error': 'must be 10 digit number'})
        

        try:
            amount=float(amount)
            
            # hash the password before saving:
            encoded_bytes=password1.encode('utf-8')
            password1=sha256(encoded_bytes).hexdigest()

            # create_bank_account
            bank_ac=Bank(fullname=fullname,email=email,phone=phone,password=password1,amount=amount,nagrita_no=nagrita_no)

            # save bank account
            bank_ac.save()
            return JsonResponse({'success':'Bank aacount created successfully !'})

        except:
            return JsonResponse({'error':'some error occured'})


    return JsonResponse({'error':"only post request is available"})

@csrf_exempt
def load_with_bank_account(request):
    if request.method=='POST':
        account_number = request.POST['account_number']
        password = request.POST['password']
        amount = request.POST['amount']
        user=request.user
        # print(user)
        # print(User_amount.objects.get(user=user).amount)
        
        try:
            # hash the password before checking:
            encoded_bytes=password.encode('utf-8')
            password=sha256(encoded_bytes).hexdigest()
            # check if bank aacount exists
            if Bank.objects.filter(account_number=account_number).exists():
                bank_ac=Bank.objects.get(account_number=account_number)
                
                if bank_ac.password==password :
                    # check if amount is valid
                    amount=float(amount)
                    if bank_ac.amount < amount:
                        return JsonResponse({'error':'Insufficient balance in your bank account'})
                    else:
                        # decrease amount in bank account
                        bank_ac.amount = bank_ac.amount - amount

                        # increase amount in user account(app user)
                        user_amount_instance=User_amount.objects.get(user=user)
                        user_amount_instance.amount = user_amount_instance.amount + amount
                    
                        # print(user_amount_instance.amount,bank_ac.amount)

                        # TODO:transaction history

                        # save after all changes
                        bank_ac.save()
                        user_amount_instance.save()

                        return JsonResponse({'success':f'NPR {amount} amount loaded successfully'})
            
                else:
                    return JsonResponse({'error':'Password doesnot match'})
            else:
                return JsonResponse({'error':'No such user exists'})
        except:
            return JsonResponse({'error':'some error occured'})
    return JsonResponse({'error':"only post request is available"})