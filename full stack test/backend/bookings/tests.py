
from django.test import TestCase, Client
from django.urls import reverse
from .models import Appointment
import json

class AppointmentAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create a sample appointment for testing
        Appointment.objects.create(
            name="John Doe",
            phone="1234567890",
            date="2025-02-22",
            time="10:00 AM"
        )

    # --- Tests for /api/slots/ ---
    def test_get_available_slots_valid_date(self):
        # Test fetching slots for a date with no bookings
        response = self.client.get('/api/slots/?date=2025-02-23')
        self.assertEqual(response.status_code, 200)
        self.assertIn('slots', response.json())
        self.assertGreater(len(response.json()['slots']), 0)
        self.assertNotIn('1:00 PM', response.json()['slots'])  # Break time excluded

    def test_get_available_slots_booked_slot(self):
        # Test fetching slots where a slot is already booked
        response = self.client.get('/api/slots/?date=2025-02-22')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('10:00 AM', response.json()['slots'])  # Already booked

    def test_get_available_slots_invalid_date(self):
        # Test invalid date format
        response = self.client.get('/api/slots/?date=invalid-date')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    # --- Tests for /api/book/ ---
    def test_book_appointment_valid(self):
        # Test valid booking
        data = {
            'name': 'Jane Smith',
            'phone': '9876543210',
            'date': '2025-02-23',
            'time': '11:00 AM'
        }
        response = self.client.post(
            '/api/book/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue(Appointment.objects.filter(name='Jane Smith').exists())

    def test_book_appointment_duplicate(self):
        # Test double-booking the same slot
        data = {
            'name': 'John Doe',
            'phone': '1234567890',
            'date': '2025-02-22',
            'time': '10:00 AM'  # Already exists in setUp
        }
        response = self.client.post(
            '/api/book/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_book_appointment_missing_fields(self):
        # Test missing required fields (e.g., name)
        data = {
            'phone': '9876543210',
            'date': '2025-02-23',
            'time': '11:00 AM'
        }
        response = self.client.post(
            '/api/book/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())