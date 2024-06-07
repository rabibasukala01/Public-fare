from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import User_amount,User_Transaction_history,Scanned
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from . calculations import distance_duration_calculation
from . aes_decryption import decrypt_data
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
                    'distance_covered':user_history.distance_covered,
                    'expected_time_to_reach':user_history.expected_time_to_reach
                })

            return JsonResponse(history,safe=False)
        return JsonResponse({'error':'No user found'})

    except Exception as e:
        # print(e)
        return JsonResponse({'error':'No user found'})


@csrf_exempt
def scanned(request,mode):
    if request.method=='POST':
        data=json.loads(request.body)
        number=data['nfc_id']
        gps_id=data['gps_id']
        lat=float(data['lat'])
        lng=float(data['lng'])
        

        # decrypt the nfc_id
        try:
            number=decrypt_data(number)[:10]  #16 bytes, but need only 10 bytes
            # print(number)
        except:
            return JsonResponse({'error':'Invalid NFC ID'})

        if mode=='in':
            print('in')
            try:
                user_obj=User.objects.get(username=number)  
                print(user_obj)
                # create a scanned object
                tracker=False
                Scanned.objects.create(user=user_obj,gps_id=gps_id,first_coords=f"{lng},{lat}",tracker=tracker)
                # TODO : RETURN SOMETHING IMP TO CLIENT
                return JsonResponse({'success':'created 1st scan'})
            except:
                return JsonResponse({'error':'No user found'})
            
        elif mode=='out':
            try:
                user_obj=User.objects.get(username=number)  
                scanned_obj=Scanned.objects.filter(user=user_obj,gps_id=gps_id,tracker=False).order_by('-scanned_datetime').first()
                scanned_obj.second_coords=f"{lng},{lat}"
                # calculate distance and time
                duration,distance=distance_duration_calculation(scanned_obj.first_coords,scanned_obj.second_coords)
                scanned_obj.distance_covered=distance
                scanned_obj.expected_time_to_reach=duration
                scanned_obj.tracker=True

                # TODO:calculate amount
                amount=round(distance*0.1,2)
                scanned_obj.transcation_amount=amount
                
                
                # update user amount
                user_amount=User_amount.objects.get(user=user_obj)
                # check if user has enough balance to pay
                if user_amount.amount<=amount:
                    return JsonResponse({'error':'Insufficient balance','balance':user_amount.amount})

                user_amount.amount=round(user_amount.amount-amount,2)
                user_amount.last_transaction=timezone.now()

                # create a transaction history
                User_Transaction_history.objects.create(user=user_obj,transaction_amount=amount,pickup_point_latitude=scanned_obj.first_coords.split(',')[1],pickup_point_longitude=scanned_obj.first_coords.split(',')[0],drop_point_latitude=scanned_obj.second_coords.split(',')[1],drop_point_longitude=scanned_obj.second_coords.split(',')[0],distance_covered=distance,expected_time_to_reach=duration)
                 
                # save objects
                scanned_obj.save()
                user_amount.save()

                # TODO : RETURN SOMETHING IMP TO CLIENT
                return JsonResponse({'success':'paid','amount':amount})
            except Exception as e:
                print(e)
                return JsonResponse({'error':'error occured'})

        else:
            return JsonResponse({'error':'Invalid url'})

    
    return JsonResponse({'error':'POST ONLY'})