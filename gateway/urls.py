from django.urls import path
from . import views

urlpatterns = [
    path('send_amount',views.send_amount,name='send_amount'),
]
