from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from src.booking.models import FitnessModel, BookingModel, InstructorModel
from django.utils import timezone
from datetime import time

class FitnessClassTests(APITestCase):
    def setUp(self):
        self.url = reverse('class-list')  # Maps to /api/classes/
        self.instructor = InstructorModel.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            bio="Experienced yoga instructor"
        )
        self.fitness_data = {
            'name': 'YOGA',
            'description': 'Morning yoga session',
            'instructor': self.instructor.id,
            'datetime_ist': (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            'duration_minutes': 60,
            'total_slots': 15,
            'available_slots': 15,
            'days_of_week': ['MON','WED','THU'],
        }

    def test_create_fitness_class(self):
        response = self.client.post(self.url, self.fitness_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'YOGA')
        self.assertIn('id', response.data)

    def test_get_fitness_classes(self):
        FitnessModel.objects.create(
            name='YOGA',
            description='Morning yoga session',
            instructor=self.instructor,
            datetime_ist=timezone.now() + timezone.timedelta(days=1),
            duration_minutes=60,
            total_slots=15,
            available_slots=15,
            days_of_week='MON,WED,THU',
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class BookingTests(APITestCase):
    def setUp(self):
        self.instructor = InstructorModel.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            bio="Experienced yoga instructor"
        )
        self.fitness = FitnessModel.objects.create(
            name='HIIT',
            description='High-intensity interval training',
            instructor=self.instructor,
            datetime_ist=timezone.now() + timezone.timedelta(days=1),
            duration_minutes=60,
            total_slots=20,
            available_slots=20,
            days_of_week='TUE,THU',
        )
        self.booking_data = {
            'fitness_id': self.fitness.id,
            'client_name': 'Alice',
            'client_email': 'alice@example.com'
        }
        self.url = reverse('booking-create')  # Maps to /api/bookings/

    def test_create_booking(self):
        response = self.client.post(self.url, self.booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['client_name'], 'Alice')
        self.assertEqual(response.data['client_email'], 'alice@example.com')
        self.assertIn('id', response.data)

    def test_get_booking_by_email(self):
        BookingModel.objects.create(
            fitness=self.fitness,
            client_name='Bob',
            client_email='bob@example.com'
        )
        response = self.client.get(reverse('booking-list'), {'client_email': 'bob@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_booking_missing_email(self):
        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)