from django.test import TestCase
from django.utils import timezone
from src.booking.models import InstructorModel, FitnessModel, BookingModel
from src.booking.serializer import BookingSerializer

class FitnessClassModelTest(TestCase):
    def setUp(self):
        self.instructor = InstructorModel.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            bio="Experienced yoga instructor"
        )
        self.fitness_class = FitnessModel.objects.create(
            name="YOGA",
            description="Morning yoga session",
            instructor=self.instructor,
            datetime_ist=timezone.now() + timezone.timedelta(days=1),
            duration_minutes=60,
            total_slots=20,
            available_slots=20,
            days_of_week=['MON','WED','THU']
        )

    def test_fitness_class_creation(self):
        self.assertEqual(self.fitness_class.name, "YOGA")
        self.assertEqual(self.fitness_class.instructor.name, "Jane Doe")
        self.assertEqual(self.fitness_class.days_of_week, ["MON", "WED", "THU"])
        self.assertEqual(self.fitness_class.available_slots, 20)

    def test_fitness_class_ordering(self):
        class2 = FitnessModel.objects.create(
            name="ZUMBA",
            description="Evening zumba",
            instructor=self.instructor,
            datetime_ist=timezone.now() + timezone.timedelta(days=2),
            duration_minutes=60,
            total_slots=20,
            available_slots=20,
            days_of_week=["TUE", "THU"]
        )
        classes = FitnessModel.objects.all()
        self.assertEqual(list(classes), [self.fitness_class, class2])


class BookingModelTest(TestCase):
    def setUp(self):
        self.instructor = InstructorModel.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            bio="Experienced yoga instructor"
        )
        self.fitness_class = FitnessModel.objects.create(
            name="YOGA",
            description="Morning yoga session",
            instructor=self.instructor,
            datetime_ist=timezone.now() + timezone.timedelta(days=1),
            duration_minutes=60,
            total_slots=20,
            available_slots=20,
            days_of_week=['MON', 'WED', 'THU']
        )

    def create_booking(self, client_name, client_email):
        data = {
            "fitness_id": self.fitness_class.id,
            "client_name": client_name,
            "client_email": client_email
        }
        serializer = BookingSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.fitness_class.refresh_from_db()
        return serializer.instance

    def test_booking_creation(self):
        booking = self.create_booking("John Smith", "john@example.com")
        self.assertEqual(booking.client_name, "John Smith")
        self.assertEqual(booking.fitness, self.fitness_class)
        self.assertEqual(booking.status, "CONFIRMED")
        self.assertEqual(self.fitness_class.available_slots, 19)

    def test_booking_creation_success_for_new_email(self):
        self.create_booking("John Smith", "john@example.com")
        self.create_booking("Jane Smith", "jane.smith@example.com")
        self.assertEqual(BookingModel.objects.count(), 2)
        self.assertEqual(self.fitness_class.available_slots, 18)

    def test_booking_ordering(self):
        booking1 = self.create_booking("John Smith", "john@example.com")
        booking2 = self.create_booking("Jane Smith", "jane.smith@example.com")
        bookings = BookingModel.objects.all()
        self.assertEqual(list(bookings), [booking1, booking2])

    def test_unique_booking_per_class_and_email(self):
        self.create_booking("John Smith", "john@example.com")
        with self.assertRaises(Exception):
            self.create_booking("John Smith", "john@example.com")
