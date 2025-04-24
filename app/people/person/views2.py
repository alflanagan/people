from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Person, PersonAddress, PersonPhone
from address.models import Address
from .serializers import PersonSerializer, PersonAddressSerializer, PersonPhoneSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=True, methods=['post'])
    def add_address(self, request, pk=None):
        """Add an address to a person"""
        person = self.get_object()

        # Check if address already exists or create a new one
        address_data = request.data.get('address', {})
        address_id = address_data.get('id')

        if address_id:
            try:
                address = Address.objects.get(id=address_id)
            except Address.DoesNotExist:
                return Response(
                    {"error": "Address not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Create new address
            from address.serializers import AddressSerializer
            address_serializer = AddressSerializer(data=address_data)
            if address_serializer.is_valid():
                address = address_serializer.save()
            else:
                return Response(
                    address_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create the relationship
        label = request.data.get('label', 'Home')

        # Check if relationship already exists
        if PersonAddress.objects.filter(person=person, address=address).exists():
            return Response(
                {"error": "This address is already associated with this person"},
                status=status.HTTP_400_BAD_REQUEST
            )

        person_address = PersonAddress.objects.create(
            person=person,
            address=address,
            label=label
        )

        serializer = PersonAddressSerializer(person_address)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove_address(self, request, pk=None):
        """Remove an address from a person"""
        person = self.get_object()
        address_id = request.data.get('address_id')

        try:
            person_address = PersonAddress.objects.get(
                person=person,
                address_id=address_id
            )
            person_address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PersonAddress.DoesNotExist:
            return Response(
                {"error": "This address is not associated with this person"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def add_phone(self, request, pk=None):
        """Add a phone number to a person"""
        person = self.get_object()

        phone = request.data.get('phone')
        label = request.data.get('label', 'Mobile')

        if not phone:
            return Response(
                {"error": "Phone number is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if phone already exists for this person
        if PersonPhone.objects.filter(person=person, phone=phone).exists():
            return Response(
                {"error": "This phone number is already associated with this person"},
                status=status.HTTP_400_BAD_REQUEST
            )

        person_phone = PersonPhone.objects.create(
            person=person,
            phone=phone,
            label=label
        )

        serializer = PersonPhoneSerializer(person_phone)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove_phone(self, request, pk=None):
        """Remove a phone number from a person"""
        person = self.get_object()
        phone_id = request.data.get('phone_id')

        try:
            person_phone = PersonPhone.objects.get(
                person=person,
                id=phone_id
            )
            person_phone.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PersonPhone.DoesNotExist:
            return Response(
                {"error": "This phone number is not associated with this person"},
                status=status.HTTP_404_NOT_FOUND
            )
