from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Person, PersonAddress, PersonPhone
from .serializers import PersonSerializer, PersonAddressSerializer, PersonPhoneSerializer

class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows people to be viewed, created, edited, or deleted.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'nickname', 'birthday']
    search_fields = ['name', 'nickname']
    ordering_fields = ['name', 'birthday', 'first_contact']

    @action(detail=True, methods=['post'])
    def add_address(self, request, pk=None):
        person = self.get_object()
        # Implementation for adding an address to a person
        # This would need to be expanded based on your actual model structure
        return Response({'status': 'address added'})

    @action(detail=True, methods=['post'])
    def add_phone(self, request, pk=None):
        person = self.get_object()
        # Implementation for adding a phone to a person
        return Response({'status': 'phone added'})
