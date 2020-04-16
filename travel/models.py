from django.db import models 

class Travel(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    start_lat = models.DecimalField(max_digits=20, decimal_places=10)
    start_lng = models.DecimalField(max_digits=20, decimal_places=10)

    end_lat = models.DecimalField(max_digits=20, decimal_places=10)
    end_lng = models.DecimalField(max_digits=20, decimal_places=10)

    travel_type_1 = models.CharField(max_length=100, null=True)
    travel_type_2 = models.CharField(max_length=100, null=True)

class TravelWayPoints(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=20, decimal_places=10)
    lng = models.DecimalField(max_digits=20, decimal_places=10)

class TravelTransit(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=20, decimal_places=10)
    lng = models.DecimalField(max_digits=20, decimal_places=10)

