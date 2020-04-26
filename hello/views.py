from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import flights,passengers
# Create your views here.
def index(request):
    context={
    'flights':flights.objects.all()
    }
    return render(request,'flights/index.html',context)
def flight(request,flight_id):
    try:
        flight = flights.objects.get(pk=flight_id)
    except flights.DoesNotExist:
        raise Http404('flight does not exist')
    context={
    'flight':flights.objects.get(pk=flight_id),
    'passengers':flights.objects.get(pk=flight_id).passenger.all(),
    'non_passengers':passengers.objects.exclude(flights=flight).all()
    }
    return render(request,'flights/flights.html',context)
def book(request,flight_id):
    try:
        passenger_id= int(request.POST['passenger'])
        passenger=passengers.objects.get(pk=passenger_id)
        flight=flights.objects.get(pk=flight_id)
    except KeyError:
        return render(request,'flights/error.html',{'messag:no selection.'})
    except passengers.DoesNotExist:
        return render(request,'flights/error.html',{'messag:no flight.'})
    except passengers.DoesNotExist:
        return render(request,'flights/error.html',{'messag:no passengers.'})
    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse('flight', args=(flight_id,)))
