
from django.contrib import admin
from django.urls import path, include
from bookings.views import available_slots, book_appointment
from bookings.views import booking_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/slots/', available_slots, name='available_slots'),
    path('api/book/', book_appointment, name='book_appointment'),
    path('api/slots/', include('bookings.urls')),  # Include your app's API URLs
    path('api/book/', include('bookings.urls')),   # Include your app's API URLs
    path('', booking_view, name='home'),
]
