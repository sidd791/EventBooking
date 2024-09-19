from rest_framework import serializers
from .models import User, EventOrganizer, Customer, Ticket, Booking, Event


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            role=validated_data["role"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        if user.role == 'customer':
            Customer.objects.create(user=user)
        elif user.role == 'organizer':
            EventOrganizer.objects.create(user=user)

        return user


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["event_organizer", "name", "venue", "date", "id"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["name", "contact_info"]


class EventOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizer
        fields = ["name", "contact_info", "organization"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["event", "customer", "ticket", "quantity", "date"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["event", "price", "ticket_type", "availability", "id"]
