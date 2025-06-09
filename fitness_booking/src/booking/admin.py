from django.contrib import admin
from django import forms
from .models import InstructorModel, FitnessModel, BookingModel

@admin.register(InstructorModel)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    ordering=['-id']


@admin.register(BookingModel)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_email', 'fitness', 'booked_at', 'status']
    list_filter = ['status', 'fitness']
    search_fields = ['client_name', 'client_email']
    list_per_page = 10
    ordering=['-id']
    


class FitnessModelForm(forms.ModelForm):
    days_of_week = forms.MultipleChoiceField(
        choices=FitnessModel.DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,  
        required=False,
    )

    class Meta:
        model = FitnessModel
        fields = '__all__'


@admin.register(FitnessModel)
class FitnessModelAdmin(admin.ModelAdmin):
    form = FitnessModelForm
    list_display = ('name', 'instructor', 'days_of_week')
    ordering=['-id']
