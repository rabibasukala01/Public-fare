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
    history=[]
    try:
        user=User.objects.get(id=pk)
        # print(user)
        if user is not None:
            user_historys=User_Transaction_history.objects.filter(user=user)
            # print(user_historys)
            for user_history in user_historys:
                history.append({
                    'transaction_amount':user_history.transaction_amount,
                    'transaction_datetime':  user_history.transaction_datetime,
                    "pickup_point_latitude":user_history.pickup_point_latitude ,
                    'pickup_point_longitude':user_history.pickup_point_longitude ,
                    "drop_point_latitude":user_history.drop_point_latitude ,
                    'drop_point_longitude':user_history.drop_point_longitude ,
                    'distance_covered':user_history.distance_covered
                })

            return JsonResponse(history,safe=False)
        return JsonResponse({'error':'No user found'})

    except Exception as e:
        # print(e)
        return JsonResponse({'error':'No user found'})


def scanned(request,number):
    if request.method=='POST':
        data=request.body
        # print(data)
        try:
            number=data['nfc_id']
            gps_id=data['gps_id']
            lat=data['lat']
            lng=data['lng']
            print(number,gps_id,lat,lng)
            obj=User.objects.get(username=number)
            print(obj)
            # TODO : HISTORY
            # User_Transaction_history.objects.create(user=user,transaction_amount=int(data['amount']),pickup_point_latitude=data['pickup_point_latitude'],pickup_point_longitude=data['pickup_point_longitude'],drop_point_latitude=data['drop_point_latitude'],drop_point_longitude=data['drop_point_longitude'],distance_covered=data['distance_covered'])
        except:
            return JsonResponse({'error':'No user found'})
        return

    return JsonResponse({'message':'Scanned Successfully'})
    return JsonResponse({'error':'POST ONLY'})