
from django.urls import path
from .views import available_slots, book_appointment, booking_view

urlpatterns = [
    # API endpoints
    path('api/slots/', available_slots, name='available_slots'),
    path('api/book/', book_appointment, name='book_appointment'),
    
    # Booking page (user interface)
    path('book/', booking_view, name='booking_view'),
]