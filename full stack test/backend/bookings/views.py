
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Appointment
import json
from datetime import date
from django.shortcuts import render



def booking_view(request):
    return render(request, 'bookings/booking.html') 

def generate_time_slots():
    # Generate slots from 10:00 AM to 5:00 PM, excluding 1:00 PM to 2:00 PM
    slots = []
    for hour in [10, 11, 12, 14, 15, 16]:  # Skip 13 (1 PM)
        for minute in ['00', '30']:
            time = f"{hour}:{minute} AM" if hour < 12 else f"{hour-12 if hour > 12 else 12}:{minute} PM"
            slots.append(time)
    return slots

@csrf_exempt
def available_slots(request):
    if request.method == 'GET':
        selected_date = request.GET.get('date')
        existing_bookings = Appointment.objects.filter(date=selected_date).values_list('time', flat=True)
        all_slots = generate_time_slots()
        available = [slot for slot in all_slots if slot not in existing_bookings]
        return JsonResponse({'slots': available})

@csrf_exempt
def book_appointment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        phone = data.get('phone')
        date_str = data.get('date')
        time = data.get('time')

        # Check if slot is already booked
        if Appointment.objects.filter(date=date_str, time=time).exists():
            return JsonResponse({'error': 'Slot already booked!'}, status=400)

        # Save appointment
        Appointment.objects.create(
            name=name,
            phone=phone,
            date=date_str,
            time=time
        )
        return JsonResponse({'status': 'success'})