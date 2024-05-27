from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import RealTimecoords
# Create your views here.


# post method testing for esp32
@csrf_exempt
def test(request):
    if request.method == 'POST':
        print(json.loads(request.body))
        return JsonResponse({'message':'here is posted data'})
    return JsonResponse({'message':'GET method is not allowed'})

@csrf_exempt
def update_coords(request):
    if request.method == 'POST':
        data= json.loads(request.body)
        try:
            # from post
            gps_id =data['gps_id']
            obj=RealTimecoords.objects.get(gps_uid=gps_id)
            obj.lat=data['lat']
            obj.lng=data['lng']
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
