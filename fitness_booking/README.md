Fitness Studio Booking API

This project implements a simple Booking API for a fictional fitness studio using Python and Django REST Framework. It allows clients to view upcoming fitness classes, book a spot, retrieve their bookings, and cancel bookings. The API supports timezone management, input validation, logging, and includes unit tests.

Features

View Upcoming Classes: Retrieve a list of upcoming fitness classes with details like name, date/time, instructor, and available slots (GET /api/classes/).
Book a Class: Submit a booking request for a class with validation for slot availability (POST /api/book/).
View Bookings: Retrieve all bookings made by a specific email address (GET /api/bookings/).
Cancel a Booking: Cancel a booking and free up a slot in the associated class (PATCH /api/bookings/<id>/cancel/).
Timezone Management: Classes are created in IST (Asia/Kolkata), and the API adjusts the displayed time based on the user's timezone.
Error Handling: Includes validation for missing fields, overbooking, duplicate bookings, and unauthorized cancellations.
Logging: Logs API requests, errors, and seeding operations for debugging.
Unit Tests: Includes tests for class creation, booking creation, booking retrieval, and cancellation.

Tech Stack

Backend: Python , Django , Django REST Framework
Database: SQLite
Dependencies: Managed via poetry.lock and pyproject.toml
Timezone Handling: Uses pytz for timezone conversion

Prerequisites
Before setting up the project, ensure you have the following installed:

Python 3.9 or higher
Poetry (dependency manager for Python)
cURL or Postman (for testing API endpoints)

Setup Instructions
Follow these steps to set up and run the project locally.
1. Clone the Repository
Clone the project repository to your local machine:
git clone <repository-url>
cd fitness_booking
set PYTHONPATH=.

2. Install Dependencies
This project uses Poetry to manage dependencies. Install the required packages:
poetry install


3. Apply Database Migrations
Set up the SQLite database by running migrations:
poetry run python src/manage.py migrate

4. Seed the Database (Optional)
The project includes a script to populate the database with sample data (instructors, classes, and bookings). To seed the database:
poetry run python temp/seed.py

This will:

Create sample instructors, fitness classes, and bookings.
Log the seeding process for debugging.

5. Run the Development Server
Start the Django development server:
poetry run python src/manage.py runserver

The API will be available at http://localhost:8000.
API Endpoints
The API exposes the following endpoints:
1. GET /api/classes/
Retrieve a list of upcoming fitness classes.
Query Parameters

user_timezone (optional): The timezone to display class times in (e.g., America/New_York). Defaults to Asia/Kolkata.

Sample Request
curl -X GET "http://localhost:8000/api/classes/?user_timezone=America/New_York"

Sample Response
[
  {
    "id": 1,
    "name": "YOGA",
    "description": "Morning yoga session",
    "instructor": {
      "id": 1,
      "name": "Jane Doe",
      "email": "jane@example.com"
    },
    "start_time": "22:30:00",
    "start_date": "2025-06-10",
    "duration_minutes": 60,
    "total_slots": 20,
    "available_slots": 18,
    "days_of_week": ["MON", "WED", "THU"]
  }
]

2. POST /api/book/
Book a spot in a fitness class.
Request Body

fitness_id (required): ID of the fitness class to book.
client_name (required): Name of the client.
client_email (required): Email of the client.

Sample Request
curl -X POST http://localhost:8000/api/book/ \
  -H "Content-Type: application/json" \
  -d '{"fitness_id": 1, "client_name": "Alice Johnson", "client_email": "alice@example.com"}'

Sample Response
{
  "id": 1,
  "fitness": "Yoga with Jane Doe on MON, WED, THU at 09:00:00",
  "fitness_id": 1,
  "client_name": "Alice Johnson",
  "client_email": "alice@example.com",
  "booked_at": "2025-06-09T12:42:00Z",
  "status": "CONFIRMED"
}

Error Responses

No slots available:{"error": "No slots available for this class."}


Duplicate booking (same email for the same class):{"error": "You have already booked this class."}


Missing fields:{"client_email": ["This field is required."]}



3. GET /api/bookings/
Retrieve all bookings for a specific client email.
Query Parameters

client_email (required): The email address of the client.

Sample Request
curl -X GET "http://localhost:8000/api/bookings/?client_email=alice@example.com"

Sample Response
[
  {
    "id": 1,
    "fitness": "Yoga with Jane Doe on MON, WED, THU at 09:00:00",
    "client_name": "Alice Johnson",
    "client_email": "alice@example.com",
    "booked_at": "2025-06-09T12:42:00Z",
    "status": "CONFIRMED"
  }
]

Error Responses

Missing client_email:{"error": "client_email is required"}



4. PATCH /api/bookings/<id>/cancel/
Cancel a booking and free up a slot in the fitness class.
Request Body

client_email (required): Email of the client cancelling the booking.

Sample Request
curl -X PATCH http://localhost:8000/api/bookings/1/cancel/ \
  -H "Content-Type: application/json" \
  -d '{"client_email": "alice@example.com"}'

Sample Response
{
  "id": 1,
  "fitness": "Yoga with Jane Doe on MON, WED, THU at 09:00:00",
  "client_name": "Alice Johnson",
  "client_email": "alice@example.com",
  "booked_at": "2025-06-09T12:42:00Z",
  "status": "CANCELLED"
}

Error Responses

Unauthorized:{"error": "You are not authorized to cancel this booking."}


Already cancelled:{"error": "Booking is already cancelled."}


Booking not found:{"error": "Booking not found."}


Missing client_email:{"error": "client_email is required for cancellation."}



Running Unit Tests
The project includes unit tests for the API endpoints. To run the tests:
python manage.py test

This will run tests for:

Creating and listing fitness classes.
Creating and retrieving bookings.
Cancelling bookings.
Handling edge cases like missing email in GET /bookings/ and unauthorized cancellations.

Project Structure

src/booking/: Contains the main application code (models, serializers, views, URLs).
src/config/: Django project settings and URL configurations.
tests/: Unit tests for the API endpoints.
temp/seed: which contain script code to create instance for all models
manage.py: Script to seed the database with sample data.
pyproject.toml and poetry.lock: Dependency management files.
db.sqlite3: SQLite database file.

Security Notes

The ALLOWED_HOSTS setting in settings.py is set to ['*'] for development. In production, update this to specific domains (ALLOWED_HOSTS = ['yourdomain.com']) to prevent security risks.
The SECRET_KEY in settings.py is hardcoded for development. In production, store it in an environment variable.

Troubleshooting

Timezone issues: Ensure the user_timezone query parameter is a valid timezone name (e.g., America/New_York). Invalid timezones will default to Asia/Kolkata.
Booking errors: If you encounter overbooking issues, ensure there are available slots before booking. The API prevents overbooking but does not handle concurrent requests atomically (a potential improvement).
Cancellation errors: Ensure the client_email matches the booking’s email to authorize cancellation.
Logs: Check the console logs for debugging information (e.g., API errors, seeding logs).

Future Improvements

Implement atomic transactions to prevent race conditions during booking.
Add more unit tests for timezone conversion and edge cases.
Add API documentation using Swagger/OpenAPI (e.g., with drf-yasg).

Author
This project was developed as part of a Python Developer Assignment for a role requiring 1+ years of experience.
