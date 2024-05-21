from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from fare.models import *
from django.contrib.auth.models import User
from bank.models import *

from hashlib import sha256


@csrf_exempt
def bank_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        try:
            bank_ac = Bank.objects.get(phone=phone)

            # hash the password before comparing
            password = password.encode('utf-8')
            if bank_ac.password == sha256(password).hexdigest():

                # Set session variable to mark the user as logged in
                request.session['bank_id'] = bank_ac.id
                # return JsonResponse({'success': 'logged in'})
                return redirect('send_amount')
            
        except Bank.DoesNotExist:
            return JsonResponse({'error': 'Account related to this phone not found'})
    
        return JsonResponse({'error': 'Invalid credentials'})
    
    return render(request, 'bank_login.html')

def bank_logout(request):
    # Clear the session to log out the user
    request.session.clear()
    return redirect('bank_login')  # Redirect to the login page


@csrf_exempt
def send_amount(request):

    '''
    Check if the user is logged in
    bank_id=request.session.get('bank_id')
    bank_ac = Bank.objects.get(id=bank_id)
    '''
    context={
        'bank_id':None,
        'fullname':'',
        'amount':'',
        'account_number':''

    }
    bank_id = request.session.get('bank_id')
    if bank_id:
        context['bank_id']=bank_id
        context['amount']=Bank.objects.get(id=bank_id).amount
        context['fullname']=Bank.objects.get(id=bank_id).fullname
        context['account_number']=Bank.objects.get(id=bank_id).account_number
        context['phone']=Bank.objects.get(id=bank_id).phone



    print(bank_id)
    if request.method == 'POST':
        
        if not bank_id:
            messages.error(request, f'Error: You must be logged in to send amount')
            return render(request, 'send_amount.html')
        
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        bank_ac = Bank.objects.get(id=bank_id)
        try:
            # check if the user exists

            if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():

                if '@' in email:
                    user = User.objects.get(email=email)
                else:
                    user = User.objects.get(username=email)   #here email will be number(whicj is acting as username in db)
                
                # deduct own amount from bank account
                if bank_ac.amount < float(amount):
                    messages.error(request, f'Error: Insufficient balance in your Bank account')
                    return render(request, 'send_amount.html',context)
                
                bank_ac.amount =bank_ac.amount - float(amount)

                # add amount to respective user
                user_amount = User_amount.objects.get(user=user)
                user_amount.amount += float(amount)
                
                # save the changes
                bank_ac.save()
                user_amount.save()

                messages.success(request,f'Success: NRP {amount} sent to {email}') 
                # return JsonResponse({'success':f'NRP {amount} sent to {email}'})    
                return render(request, 'send_amount.html',context)
            
        except User.DoesNotExist:
            messages.error(request, f"Error: User '{email}' not found")
            # return JsonResponse({'error':f'User {email} not found'} )
            return render(request, 'send_amount.html',context)
        except Exception as e:
            messages.error(request, f"An error occurred")
            return render(request, 'send_amount.html',context)
            # return JsonResponse({'error':f'some error occured - {e}'})

    return render(request, 'send_amount.html',context)