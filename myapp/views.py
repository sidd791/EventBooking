from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Event, Ticket, Booking
from .permissions import IsEventOrganizer
from .serializers import EventSerializer, TicketSerializer, BookingSerializer
from .tasks import booking_confirmation, event_update
from rest_framework import serializers


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class EventView(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsEventOrganizer]

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        response = super().update(request, *args, **kwargs)
        updated_event = self.get_object()

        # Send a single task with all the necessary information
        event_update.delay(
            event_name=updated_event.name,
            changes=request.data,
            email = request.user.email
        )

        return response


class TicketView(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsEventOrganizer]


class BookingView(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.role == 'customer':
            raise serializers.ValidationError("Only customers can create bookings.")

        customer = self.request.user.customer
        booking = serializer.save(customer=customer)

        booking_confirmation.delay(
            email=self.request.user.email,
            event_name=booking.event.name,
            ticket_type=booking.ticket.ticket_type,
            quantity=booking.quantity,
        )


