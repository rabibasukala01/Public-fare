from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import RealTimecoords,GPS_ID
# Create your views here.


@csrf_exempt
def update_coords(request):
    if request.method == 'POST':
        data= json.loads(request.body)
        # print(data) 
        try:
            # from post
            gps_id = int(data['gps_id'])
            lat=float(data['lat'])
            lng=float(data['lng'])
            print(gps_id,lat,lng)
            gps_obj=GPS_ID.objects.get(gps_uid=gps_id)
            print("here")
            print(gps_obj)
            # Update or create RealTimecoords object
            obj, created = RealTimecoords.objects.update_or_create(
                gps_uid=gps_obj,
                defaults={
                    'lat':lat,
                    'lng':lng
                }
            )
            print(obj)
            obj.save()
            
            return JsonResponse({'status':200})
        except:
            return JsonResponse({'status':'5xx'})
        
    return JsonResponse({'error':'GET method is not allowed'})

def fetch_coords(request):
    context=[]

    try:
        instance=RealTimecoords.objects.all()

        for i in instance:
            context.append({
                'gps_uid':i.gps_uid.gps_uid,
                'lat':i.lat,
                'lng':i.lng,

            })


        return JsonResponse(context,safe=False)
    except :
        return JsonResponse({'status':500})
