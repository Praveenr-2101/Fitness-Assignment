from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessModel, BookingModel
from .serializer import FitnessClassSerializer, BookingSerializer ,FitnessCreateSerializer
import logging

logger = logging.getLogger(__name__)


class ClassListView(APIView):
    def get(self, request):
        try:
            user_tz = request.GET.get('user_timezone', 'Asia/Kolkata')
            logger.info(f"User timezone: {user_tz}")
            classes = FitnessModel.objects.all()
            serializer = FitnessClassSerializer(classes, many=True,context={'user_timezone': user_tz})
            return Response(serializer.data)
        except Exception as e:
            logger.exception("Error fetching class list")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = FitnessCreateSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info(f"Fitness class created: {serializer.validated_data.get('name')}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Unexpected error creating fitness class")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingCreateView(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            booking = serializer.save()
            logger.info(f"Booking created for {booking.client_email}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as ve:
            logger.error(f"Value error during booking: {ve}")
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected error during booking creation")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingListView(APIView):
    def get(self, request):
        email = request.query_params.get('client_email')
        if not email:
            logger.warning("Missing client_email in booking list request")
            return Response({"error": "client_email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            bookings = BookingModel.objects.filter(client_email=email)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.exception("Error retrieving bookings")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)