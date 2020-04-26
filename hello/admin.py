from django.contrib import admin
from .models import airport,flights,passengers


#new added content today 23/04/2020
class passengerinline(admin.StackedInline):
    model = passengers.flights.through

class flightadmin(admin.ModelAdmin):
    inlines = [passengerinline]
class passengeradmin(admin.ModelAdmin):
    filter_horizontal = ('flights',)
# Register your models here.
admin.site.register(airport)
admin.site.register(flights,flightadmin)
admin.site.register(passengers,passengeradmin)
