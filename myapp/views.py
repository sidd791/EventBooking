from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Event, Ticket, Booking
from .permissions import IsEventOrganizer, IsCustomer
from .serializers import EventSerializer, TicketSerializer, BookingSerializer
from .tasks import booking_confirmation, event_update


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# Create your views here.
class EventView(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsEventOrganizer]

    def perform_create(self, serializer):
        event = serializer.save()
        bookings = Booking.objects.filter(event=event)
        changes = serializer.validated_data,
        for booking in bookings:
            event_update.delay(
                email=booking.customer.user.email,
                event_name=event.name,
                changes=changes
            )


class TicketView(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsEventOrganizer]


class BookingView(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        customer = self.request.user.customer
        booking = serializer.save(customer=customer)

        booking_confirmation.delay(
            email=self.request.user.email,
            event_name = booking.event.name,
            ticket_type=booking.ticket.ticket_type,
            quantity=booking.quantity,
        )
