from django.db import models

# Create your models here.
# popup in map





class MapPopup(models.Model):
    id=models.AutoField(primary_key=True)
    route = models.CharField(max_length=255)    #ktm-bkt
    plate_no = models.CharField(max_length=255)

    def __str__(self):
        return self.plate_no

# for realtime tracking
class RealTimecoords(models.Model):
    id=models.AutoField(primary_key=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return 'idk'
