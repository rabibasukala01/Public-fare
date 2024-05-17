from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('forgetPassword/', views.forgetPassword, name='forgetPassword'),
    path('resetPassword/<token>', views.resetPassword, name='resetPassword'),
]
