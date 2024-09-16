from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (("customer", "Customer"), ("organizer", "Event organizer"))
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default="customer")


class EventOrganizer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.organization


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name


class Event(models.Model):
    event_organizer = models.ForeignKey(EventOrganizer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    ticket_type = models.CharField(max_length=100)
    availability = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.event} - {self.price}"


class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f"Booking made by {self.customer} for {self.event}"
