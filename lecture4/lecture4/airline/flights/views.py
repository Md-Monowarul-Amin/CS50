from unicodedata import name
from django.shortcuts import render

import flights
from .models import Flight, Passenger
# Create your views here.

def index(request):
    print(Flight.objects.all())
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    flight_ = Flight.objects.get(pk=flight_id)
    passengers = Passenger.objects.filter(flights = flight_)
    remaining_passengers = Passenger.objects.exclude(flights = flight_)
    # print(passengers)
    # print(remaining_passengers)
    # print(len(passengers))
    # print(type(passenger))
    return render(request, "flights/flight.html", {"flight":flight_,
     "passengers": passengers, "ramaining_passengers":remaining_passengers })    


def book(request, flight_id):
    if request.method == "POST":
        passenger = Passenger.objects.get(pk= int(request.POST["passenger"])) 
        print(passenger.first_name)
        passenger.flights.add(Flight.objects.get(pk= flight_id))
        return flight(request, flight_id)
    
    else:
        print("No passenger added")
        return flight(request, flight_id)