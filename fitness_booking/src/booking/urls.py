from django.urls import path
from .views import ClassListView, BookingCreateView, BookingListView, BookingCancelView,InstructorView

urlpatterns = [
    path('classes/', ClassListView.as_view(), name='class-list'),
    path('book/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    
    #optional
    path('instructor/',InstructorView.as_view(),name='instructors'),
    path('cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]