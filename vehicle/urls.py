from django.urls import path

from . import views

from . import views
urlpatterns = [
    path('update_coords', views.update_coords, name='update_coords'),
    path('fetch_coords', views.fetch_coords, name='fetch_coords'),
]
