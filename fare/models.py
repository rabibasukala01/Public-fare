from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# user table
class User_Transaction_history(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_amount = models.FloatField(default=0.0)
    transaction_datetime = models.DateTimeField(auto_now_add=True)
    pickup_point_latitude = models.FloatField(null=True,blank=True)
    pickup_point_longitude = models.FloatField(null=True,blank=True)
    drop_point_latitude = models.FloatField(null=True,blank=True)
    drop_point_longitude = models.FloatField(null=True,blank=True)
    distance_covered = models.FloatField(null=True,blank=True)
    expected_time_to_reach=models.FloatField(blank=True,null=True)
    

    def __str__(self):
        return self.user.username

class User_amount(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    amount = models.FloatField(default=0.00)
    last_transaction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Scanned(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    gps_id = models.CharField(max_length=100)
    first_coords=models.CharField(max_length=100,blank=True,null=True)  #lng,lat
    second_coords=models.CharField(max_length=100,blank=True,null=True) #lng.lat
    distance_covered=models.FloatField(blank=True,null=True)
    expected_time_to_reach=models.FloatField(blank=True,null=True)
    transcation_amount=models.FloatField(default=0.0)
    scanned_datetime = models.DateTimeField(auto_now_add=True)
    tracker=models.BooleanField(default=False)   # to check if the user has scanned in or out ,true if scanned out

    def __str__(self): 
        return self.user.username


