from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import FitnessModel, BookingModel ,InstructorModel
from .serializer import FitnessClassSerializer, BookingSerializer ,FitnessCreateSerializer ,InstructorSerializer
import logging

logger = logging.getLogger(__name__)


class ClassListView(APIView):
    def get(self, request):
        try:
            user_tz = request.GET.get('user_timezone', 'Asia/Kolkata')
            logger.info(f"User timezone: {user_tz}")
            classes = FitnessModel.objects.all()
            serializer = FitnessClassSerializer(classes, many=True,context={'user_timezone': user_tz})
            return Response(serializer.data,status=status.HTTP_200_OK)
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
        except ValidationError as e:
            logger.warning(f"Validation failed: {e.detail}")
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
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
        except ValidationError as e:
            logger.warning(f"Booking validation failed: {e.detail}")
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
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
        
        
        
        
#Optional


class InstructorView(APIView):
    
    def get(self,request):
        try:
            Instructor=InstructorModel.objects.all()
            serializer=InstructorSerializer(Instructor,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error fetching class list")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self,request):
        
        serializer=InstructorSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.warning(f"Booking validation failed: {e.detail}")
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected error during booking creation")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
    
class BookingCancelView(APIView):
    def post(self, request):
        booking_id = request.data.get('booking_id')
        email = request.data.get('client_email')

        if not booking_id or not email:
            return Response({"error": "booking_id and client_email are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = BookingModel.objects.get(id=booking_id, client_email=email)
            if booking.status == 'CANCELLED':
                return Response({"message": "Booking already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

            booking.status = 'CANCELLED'
            booking.save(update_fields=['status'])

            booking.fitness.available_slots += 1
            booking.fitness.save(update_fields=['available_slots'])

            return Response({"message": "Booking cancelled successfully"})
        except BookingModel.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Error cancelling booking")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
