from django.contrib import admin
from .models import ParkingSlot
from .models import Parking
from .models import Booking

# Register your models here.

admin.site.register(ParkingSlot)
admin.site.register(Parking)
admin.site.register(Booking)

