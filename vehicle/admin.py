from django.contrib import admin

# Register your models here.
from .models import RealTimecoords, MapPopup

admin.site.register([RealTimecoords, MapPopup])