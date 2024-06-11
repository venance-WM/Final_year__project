from datetime import date
from django.utils.dateparse import parse_duration
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.conf import settings
from django.views.generic import TemplateView
from django.db.models import Q
from .models import Parking
from .models import Booking
from .models import ParkingSlot
from django.contrib.auth.decorators import login_required
import stripe


stripe.api_key = settings.STRIPE_SECRETE_KEY

#  My views .
def index(request):
    if 'park' in request.GET:
        park = request.GET['park']
        find_park = Q(Q(park_name__icontains=park) | Q(address__icontains=park))
        parkings = Parking.objects.filter(find_park)
        
    else:    
        parkings = Parking.objects.all()
    context={'parkings':parkings }
            
           
    return render(request, 'home/index.html',context)


def about(request):
    return render(request, 'home/about.html')


def why(request):
    return render(request, 'home/why.html')


def client(request):
    return render(request, 'home/client.html')


def pricing(request):
    return render(request, 'home/pricing.html')

def parking_detail(request, parking_id):
    parking = get_object_or_404(Parking, pk=parking_id)  # Fetch specific parking object
    parking_lots = parking.parkingslot_set.all()  # Retrieve slots related to this parking
    context = {'parking': parking, 'parking_lots': parking_lots}
    return render(request, 'bookings/parking.html', context)

def book_form(request,slot_id):
    slot = ParkingSlot.objects.get(pk=slot_id)
    user =request.user
    context = { 'slot':slot,'user':user }
    return render(request,'bookings/booking_form.html',context)

def all_parking(request):
    parkings = Parking.objects.all()
    context={'parkings':parkings }
    return render(request,'bookings/all_parking.html',context)


def place_booking(request):
    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        plate_number = request.POST.get('plate_number')
        booking_duration = parse_duration(request.POST.get('booking_duration'))
        booking_time = request.POST.get('booking_time')
        remarks = request.POST.get('remarks')
        slot = request.POST.get('slot_number')
        booking_status = request.POST.get('booking_status')
        book_new = Booking(user=request.user,car_name=car_name,booking_duration=booking_duration,booking_time=booking_time,remarks=remarks,slot=slot,booking_status=booking_status,plate_number=plate_number)
        book_new.save()
        return redirect('booked')
    else:
        messages.info(request,'You made an error please , Try again')
        return render(request,'bookings/booking_form.html')
            
        
class PaymentPageView(TemplateView):
    template_name = 'bookings/booked.html'  
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def charge(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='Payment Gateway',
            source=request.POST['stripeToken']
        )
    return render(request,'payments/charge.html')




def payment_home(request):
    return render(request,'payments/payment.html')