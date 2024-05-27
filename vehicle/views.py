from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

@csrf_exempt
def test(request):
    if request.method == 'POST':
        print(json.loads(request.body))
        return JsonResponse({'message':'here is posted data'})
    return JsonResponse({'message':'GET method is not allowed'})