from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import RealTimecoords,GPS_ID
import logging

logger = logging.getLogger(__name__)
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
        data = json.loads(request.body)
        logger.info(f"Received data for update: {data}")
        try:
            gps_id = int(data['gps_id'])
            lat = float(data['lat'])
            lng = float(data['lng'])
            gps_obj = GPS_ID.objects.get(gps_uid=gps_id)
            obj, created = RealTimecoords.objects.update_or_create(
                gps_uid=gps_obj,
                defaults={
                    'lat': lat,
                    'lng': lng
                }
            )
            obj.save()
            logger.info(f"Updated coordinates: {obj}")
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Error updating coordinates: {e}")
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'GET method is not allowed'})

def fetch_coords(request):
    context = []
    try:
        instance = RealTimecoords.objects.all()
        for i in instance:
            context.append({
                'gps_uid': i.gps_uid.gps_uid,
                'lat': i.lat,
                'lng': i.lng
            })
        logger.info(f"Fetched coordinates: {context}")
        return JsonResponse(context, safe=False)
    except Exception as e:
        logger.error(f"Error fetching coordinates: {e}")
        return JsonResponse({'error': str(e)})
