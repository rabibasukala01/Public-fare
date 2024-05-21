from django.urls import path
from . import views

urlpatterns = [
    path('send_amount',views.send_amount,name='send_amount'),
    path('bank_login',views.bank_login,name='bank_login'),
    path('bank_logout/', views.bank_logout, name='bank_logout')
]
