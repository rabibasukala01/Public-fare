from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages

from fare.models import *
from django.contrib.auth.models import User
# Create your views here.
def send_amount(request):

    if request.method == 'POST':
        amount = request.POST.get('amount')
        email = request.POST.get('email')

        try:
            if '@' in email:
                user = User.objects.get(email=email)
            else:
                user = User.objects.get(username=email)   #here email will be number(whicj is acting as username in db)
            user_amount = User_amount.objects.get(user=user)
            user_amount.amount += float(amount)
            user_amount.save()
            messages.success(request,f'Success: NRP {amount} sent to {email}')     
        except User.DoesNotExist:
            messages.error(request, f"Error: User '{email}' not found")
            return render(request, 'send_amount.html')

        return render(request, 'send_amount.html')

    return render(request, 'send_amount.html')