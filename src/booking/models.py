from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
import pytz
from pytz import timezone as pytz_timezone, UnknownTimeZoneError


class InstructorModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class FitnessModel(models.Model):
    CLASS_TYPES = [
        ('YOGA', 'Yoga'),
        ('ZUMBA', 'Zumba'),
        ('HIIT', 'HIIT'),
        ('PILATES', 'Pilates'),
    ]
    
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]


    name = models.CharField(max_length=100, choices=CLASS_TYPES)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(InstructorModel, on_delete=models.CASCADE, related_name='classes')
    datetime_ist = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60, validators=[MinValueValidator(30), MaxValueValidator(180)])
    total_slots = models.PositiveIntegerField(default=20, validators=[MinValueValidator(1), MaxValueValidator(50)])
    available_slots = models.PositiveIntegerField(default=20, validators=[MinValueValidator(0)])
    days_of_week = models.JSONField(default=list)  # e.g., 'MON,WED,THU'
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        days_str = ', '.join([dict(self.DAYS_OF_WEEK).get(day, day) for day in self.days_of_week])
        return f"{self.get_name_display()} with {self.instructor} on {days_str} at {self.datetime_ist.time()}"

    class Meta:
        ordering = ['datetime_ist']


class BookingModel(models.Model):
    fitness = models.ForeignKey(FitnessModel, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField(validators=[EmailValidator()])
    booked_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[
            ('CONFIRMED', 'Confirmed'),
            ('CANCELLED', 'Cancelled'),
        ],
        default='CONFIRMED'
    )

    def __str__(self):
        return f"Booking for {self.client_name} in {self.fitness}"

    class Meta:
        unique_together = ['fitness', 'client_email']
   