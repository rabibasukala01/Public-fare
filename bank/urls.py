from django.urls import path
from . import views
urlpatterns = [
    path('create_bank_account',views.create_bank_account,name='create_bank_account'),
    path('load_with_bank_account/<str:pk>',views.load_with_bank_account,name='load_with_bank_account')
]
