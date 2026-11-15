from django.shortcuts import render
from rest_framework import generics, viewsets, permissions

from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer


def index(request):
    """Serves the static HTML home page."""
    return render(request, 'index.html')


class MenuItemsView(generics.ListCreateAPIView):
    """GET /api/menu/  -> list menu items (public)
       POST /api/menu/ -> create a menu item (logged-in users only)"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """GET / PUT / PATCH / DELETE /api/menu/<id>/"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """Table bookings: list, create, retrieve, update, delete.
    Requires a logged-in user (token authentication)."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
