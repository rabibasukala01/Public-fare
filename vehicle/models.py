from django.db import models

# Create your models here.
# popup in map

# GPS ID is id for gps module , different id for different vehicles
class GPS_ID(models.Model):
    gps_uid=models.IntegerField(unique=True)
    def __str__(self) -> str:
        return 'GPS NUMBER [ ' + str(self.gps_uid) +' ]'


class MapPopup(models.Model):
    id=models.AutoField(primary_key=True)
    gps_uid= models.OneToOneField(GPS_ID, on_delete=models.CASCADE, unique=True,default=1)
    route = models.CharField(max_length=255)    #ktm-bkt
    plate_no = models.CharField(max_length=255)

    def __str__(self):
        return  'Plate Number: ' + self.plate_no

# for realtime tracking
class RealTimecoords(models.Model):
    id=models.AutoField(primary_key=True)
    gps_uid= models.OneToOneField(GPS_ID, on_delete=models.CASCADE, unique=True,default=1)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return 'For GPS ID [ ' + str(self.gps_uid.gps_uid)+' ]'
