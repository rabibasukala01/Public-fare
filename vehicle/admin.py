from django.contrib import admin

# Register your models here.
from .models import RealTimecoords, MapPopup,GPS_ID

admin.site.register([RealTimecoords, MapPopup,GPS_ID])