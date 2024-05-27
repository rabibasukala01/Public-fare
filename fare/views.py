from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import User_amount,User_Transaction_history

# Create your views here.
def user_info(request,pk):
    try:
        user=User.objects.get(id=pk)
        if user is not None:
            user_amount=User_amount.objects.get(user=user)
            context={
            'id':user.id,
            'fname':user.first_name,
            'lname':user.last_name,
            'phone/username':user.username,
            'email':user.email,
            'amount':user_amount.amount,

            }

            return JsonResponse(context)

    except:
        return JsonResponse({'error':'No user found'})
    
    
def user_history(request,pk):
    try:
        user=User.objects.get(id=pk)
        if user is not None:
            user_history=User_Transaction_history.objects.get(user=user)
            context={
                'transaction_amount':user_history.transaction_amount,
                  'transaction_datetime':  user_history.transaction_datetime,
    "pickup_point_latitude":user_history.pickup_point_latitude ,
    'pickup_point_longitude':user_history.pickup_point_longitude ,
    "drop_point_latitude":user_history.drop_point_latitude ,
    'drop_point_longitude':user_history.drop_point_longitude ,
    'distance_covered':user_history.distance_covered
            }

            return JsonResponse(context)

    except:
        return JsonResponse({'error':'No user found'})
