from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from myapp.views import EventView, TicketView, BookingView, RegisterView

router = DefaultRouter()
router.register(r"events", EventView, basename="event")
router.register(r"tickets", TicketView, basename="ticket")
router.register(r"bookings", BookingView, basename="booking")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    path("register/", RegisterView.as_view()),
]
