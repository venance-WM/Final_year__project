from django.db import models
from django.contrib.auth.models import User
from	django.conf	import	settings


class Parking(models.Model):
    park_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    total_spaces = models.IntegerField()
    available_spaces = models.IntegerField(default=total_spaces)  # Set default available spaces to total spaces
    hourly_fee = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    daily_fee = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.park_name
    
    
class ParkingSlot(models.Model):
    slot_number = models.IntegerField()
    is_occupied = models.BooleanField(default='empty')
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)  # Added relationship with Parking model

    def __str__(self):
        return f"Slot {self.slot_number} (Parking: {self.parking.park_name})"  # Improved string representation with parking name

    


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null = True,blank = True)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE,null = True,blank = True)  # Use `slot` for clarity (foreign key to ParkingSlot)
    car_name = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=100, unique=True,null=True)  # Added unique constraint for plate number
    booking_time = models.DateTimeField()
    booking_duration = models.DurationField()  # Use DurationField for time intervals
    booking_status = models.BooleanField(default=False)  # Default booking status to not confirmed
    remarks = models.CharField(max_length=255)

    def __str__(self):
        return f"Booking for slot number {self.slot} by {self.user.username}"  # Improved string representation with user and slot information
