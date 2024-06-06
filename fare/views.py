from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import User_amount,User_Transaction_history,Scanned
from django.views.decorators.csrf import csrf_exempt
import json
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


@csrf_exempt
def scanned(request,mode):
    print(mode)
    if request.method=='POST':
        data=json.loads(request.body)
        number=data['nfc_id']
        gps_id=data['gps_id']
        lat=data['lat']
        lng=data['lng']
        print(data)

        if mode=='in':
            print(mode,"hitted")
            try:
                user_obj=User.objects.get(username=number)  
                print(f"{lat},{lng}")
                # create a scanned object
                # Scanned.objects.create(user=user_obj,gps_id=gps_id,first_coords=f"{lat},{lng}")
                
                return JsonResponse({'success':'User found'})
            except:
                return JsonResponse({'error':'No user found'})
        elif mode=='out':
            # TODO : HISTORY
                # User_Transaction_history.objects.create(user=user,transaction_amount=int(data['amount']),pickup_point_latitude=data['pickup_point_latitude'],pickup_point_longitude=data['pickup_point_longitude'],drop_point_latitude=data['drop_point_latitude'],drop_point_longitude=data['drop_point_longitude'],distance_covered=data['distance_covered'])
            print(mode,"hitted")
            return JsonResponse({'success':'User found'})
        else:
            return JsonResponse({'error':'Invalid url'})

    
    return JsonResponse({'error':'POST ONLY'})