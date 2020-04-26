from django.db.models import Max
from django.test import Client, TestCase

from .models import airport, flights, passengers

# Create your tests here.
class flightsTestCase(TestCase):

    def setUp(self):

        # Create airports.
        a1 = airport.objects.create(code="AAA", city="City A")
        a2 = airport.objects.create(code="BBB", city="City B")

        # Create flightss.
        flights.objects.create(origin=a1, destination=a2, duration=100)
        flights.objects.create(origin=a1, destination=a1, duration=200)

    def test_departures_count(self):
        a = airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 2)

    def test_arrivals_count(self):
        a = airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = airport.objects.get(code="AAA")
        a2 = airport.objects.get(code="BBB")
        f = flights.objects.get(origin=a1, destination=a2)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
        a1 = airport.objects.get(code="AAA")
        f = flights.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = airport.objects.get(code="AAA")
        a2 = airport.objects.get(code="BBB")
        f = flights.objects.get(origin=a1, destination=a2)
        f.duration = -100
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 2)

    def test_valid_flight_page(self):
        a1 = airport.objects.get(code="AAA")
        f = flights.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = flights.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        f = flights.objects.get(pk=1)
        p = passengers.objects.create(firstna="Alice", lastna="Adams")
        f.passenger.add(p)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        f = flights.objects.get(pk=1)
        p = passengers.objects.create(firstna="Alice", lastna="Adams")

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)
