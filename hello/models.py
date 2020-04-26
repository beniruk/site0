from django.db import models

# Create your models here.


class airport(models.Model):

    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.city}({self.code})'


class flights(models.Model):
    origin = models.ForeignKey(airport, on_delete=models.CASCADE, related_name='departures')

    destination = models.ForeignKey(airport, on_delete=models.CASCADE, related_name="arrivals")

    duration = models.IntegerField()
    def is_valid_flight(self):
        return (self.origin!=self.destination) and (self.duration>=0)

    def __str__(self):
        return f'{self.id}-{self.origin},{self.destination},{self.duration}'


class passengers(models.Model):

    firstna = models.CharField(max_length=64)

    lastna = models.CharField(max_length=64)

    flights = models.ManyToManyField(flights, blank=True, related_name='passenger')

    def __str__(self):
        return f'{self.firstna} {self.lastna}'
