from django.contrib import admin
from .models import User, Customer, Event, EventOrganizer, Ticket, Booking

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Event)
admin.site.register(EventOrganizer)
admin.site.register(Ticket)
admin.site.register(Booking)
