import django
import os
import random
from datetime import datetime, timedelta
from django.utils import timezone
import logging
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings')
django.setup()

from src.booking.models import InstructorModel, FitnessModel, BookingModel
logger = logging.getLogger(__name__)


def seed_data():
    
    BookingModel.objects.all().delete()
    FitnessModel.objects.all().delete()
    InstructorModel.objects.all().delete()
    logger.info("Cleared all existing data.")

    instructors = [
        {"name": "Jane Doe", "email": "jane@example.com", "bio": "Certified Yoga and Pilates instructor"},
        {"name": "John Smith", "email": "john@example.com", "bio": "HIIT and Zumba specialist"},
        {"name": "Emma Brown", "email": "emma@example.com", "bio": "Experienced fitness coach"},
    ]

    instructor_objects = []
    for instructor in instructors:
        obj, created = InstructorModel.objects.get_or_create(
            email=instructor["email"],
            defaults={
                "name": instructor["name"],
                "bio": instructor["bio"],
                "created_at": timezone.now()
            }
        )
        instructor_objects.append(obj)
        logger.info(f"{'Created' if created else 'Found'} instructor: {obj.name}")


    class_types = ['YOGA', 'ZUMBA', 'HIIT', 'PILATES']
    days_of_week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']


    ist_tz = pytz.timezone('Asia/Kolkata')
    start_date = timezone.now().replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)

    if start_date.tzinfo is not None:
        start_date = start_date.replace(tzinfo=None)

    for i in range(10):
        class_type = random.choice(class_types)
        instructor = random.choice(instructor_objects)
        start_time = start_date + timedelta(days=i, hours=random.randint(0, 12))
        start_time = ist_tz.localize(start_time)
        days = random.sample(days_of_week, k=random.randint(1, 3))

        fitness_class = FitnessModel.objects.create(
            name=class_type,
            description=f"{class_type} session with {instructor.name}",
            instructor=instructor,
            datetime_ist=start_time,
            duration_minutes=random.choice([60, 90]),
            total_slots=20,
            available_slots=20,
            days_of_week=days,
            created_at=timezone.now()
        )
        logger.info(f"Created class: {fitness_class.name} on {fitness_class.datetime_ist}")


    clients = [
        {"name": "Alice Johnson", "email": "alice@example.com"},
        {"name": "Bob Williams", "email": "bob@example.com"},
    ]
    classes = FitnessModel.objects.all()[:3]  
    for client in clients:
        for fitness_class in classes:
            if fitness_class.available_slots > 0:
                BookingModel.objects.create(
                    fitness=fitness_class,
                    client_name=client["name"],
                    client_email=client["email"],
                    booked_at=timezone.now(),
                    status='CONFIRMED'
                )
                logger.info(f"Created booking for {client['name']} in {fitness_class.name}")


if __name__ == "__main__":
    logger.info("Seeding database...")
    seed_data()
    logger.info("Seeding complete!")