from django.urls import path


from . import views
urlpatterns = [
    path('user/<str:pk>',views.user_info,name='user_info'),
    path('user_history/<str:pk>',views.user_history,name='user_history'),
    path('scanned/<str:mode>',views.scanned,name='scanned'),
    path('mobile_scanned/<str:mode>',views.mobile_scanned,name='mobile_scanned')
]
