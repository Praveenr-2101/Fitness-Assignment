from rest_framework import serializers
from .models import FitnessModel, BookingModel, InstructorModel
from src.booking.utils import convert_to_timezone



class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorModel
        fields = ['id', 'name', 'email']

class FitnessClassSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    start_date = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()

    class Meta:
        model = FitnessModel
        fields = ['id', 'name', 'description', 'instructor', 'start_time', 'start_date', 'duration_minutes', 'total_slots', 'available_slots','days_of_week']
    
    def validate_instructor(self, value):
        if not InstructorModel.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Instructor with this ID does not exist.")
        return value
        
    def get_start_date(self, obj):
        user_tz = self.context.get('user_timezone', 'Asia/Kolkata')
        local_dt = convert_to_timezone(obj.datetime_ist, user_tz)
        return local_dt.date()

    def get_start_time(self, obj):
        user_tz = self.context.get('user_timezone', 'Asia/Kolkata')
        local_dt = convert_to_timezone(obj.datetime_ist, user_tz)
        return local_dt.time()



class BookingSerializer(serializers.ModelSerializer):
    fitness_id = serializers.PrimaryKeyRelatedField(
        queryset=FitnessModel.objects.all(),
        source='fitness',
        write_only=True
    )
    fitness = serializers.StringRelatedField(read_only=True)  # Show string representation of fitness

    class Meta:
        model = BookingModel
        fields = ['id', 'fitness', 'fitness_id', 'client_name', 'client_email', 'booked_at', 'status']
        
    def validate_fitness(self, fitness):
        if not FitnessModel.objects.filter(pk=fitness.id).exists():
            raise serializers.ValidationError("Fitness class with this ID does not exist.")
        return fitness

    def create(self, validated_data):
        fitness = validated_data['fitness']

        if fitness.available_slots <= 0:
            raise serializers.ValidationError("No slots available for this class.")

        fitness.available_slots -= 1
        fitness.save(update_fields=['available_slots'])

        booking = BookingModel.objects.create(**validated_data)
        return booking


class FitnessCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=FitnessModel
        fields="__all__"