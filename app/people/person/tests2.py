from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from person.models import Person, PersonAddress, PersonPhone
from address.models import Address
import datetime
import json

class PersonAddressPhoneTests(APITestCase):
    def setUp(self):
        """Set up test data for each test"""
        self.client = APIClient()

        # Create a test person
        self.person = Person.objects.create(
            name="John Doe",
            nickname="Johnny",
            birthday=datetime.date(1990, 1, 1),
            first_contact=datetime.date.today()
        )

        # Create a test address
        self.address = Address.objects.create(
            label="Home",
            first_line="123 Main St",
            city="Anytown",
            state="CA",
            postal_code="12345"
        )

        # API endpoints
        self.add_address_url = reverse('person-add-address', kwargs={'pk': self.person.id})
        self.remove_address_url = reverse('person-remove-address', kwargs={'pk': self.person.id})
        self.add_phone_url = reverse('person-add-phone', kwargs={'pk': self.person.id})
        self.remove_phone_url = reverse('person-remove-phone', kwargs={'pk': self.person.id})

    def test_add_existing_address_to_person(self):
        """Test adding an existing address to a person"""
        data = {
            'address': {'id': self.address.id},
            'label': 'Work'
        }
        response = self.client.post(self.add_address_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PersonAddress.objects.count(), 1)
        self.assertEqual(PersonAddress.objects.first().label, 'Work')

    def test_add_new_address_to_person(self):
        """Test adding a new address to a person"""
        data = {
            'address': {
                'label': 'Vacation Home',
                'first_line': '456 Beach Rd',
                'city': 'Beachtown',
                'state': 'FL',
                'postal_code': '33333'
            },
            'label': 'Vacation'
        }
        response = self.client.post(self.add_address_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PersonAddress.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 2)  # Original + new address

    def test_add_duplicate_address_to_person(self):
        """Test adding an address that's already associated with the person"""
        # First, add the address
        PersonAddress.objects.create(
            person=self.person,
            address=self.address,
            label='Home'
        )

        # Try to add it again
        data = {
            'address': {'id': self.address.id},
            'label': 'Work'
        }
        response = self.client.post(self.add_address_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PersonAddress.objects.count(), 1)  # Count should remain 1

    def test_remove_address_from_person(self):
        """Test removing an address from a person"""
        # First, add the address
        person_address = PersonAddress.objects.create(
            person=self.person,
            address=self.address,
            label='Home'
        )

        data = {'address_id': self.address.id}
        response = self.client.delete(self.remove_address_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PersonAddress.objects.count(), 0)

    def test_remove_nonexistent_address_from_person(self):
        """Test removing an address that's not associated with the person"""
        data = {'address_id': self.address.id}
        response = self.client.delete(self.remove_address_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_phone_to_person(self):
        """Test adding a phone number to a person"""
        data = {
            'phone': '555-123-4567',
            'label': 'Mobile'
        }
        response = self.client.post(self.add_phone_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PersonPhone.objects.count(), 1)
        self.assertEqual(PersonPhone.objects.first().phone, '555-123-4567')

    def test_add_duplicate_phone_to_person(self):
        """Test adding a phone number that's already associated with the person"""
        # First, add the phone
        PersonPhone.objects.create(
            person=self.person,
            phone='555-123-4567',
            label='Mobile'
        )

        # Try to add it again
        data = {
            'phone': '555-123-4567',
            'label': 'Work'
        }
        response = self.client.post(self.add_phone_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PersonPhone.objects.count(), 1)  # Count should remain 1

    def test_remove_phone_from_person(self):
        """Test removing a phone number from a person"""
        # First, add the phone
        person_phone = PersonPhone.objects.create(
            person=self.person,
            phone='555-123-4567',
            label='Mobile'
        )

        data = {'phone_id': person_phone.id}
        response = self.client.delete(self.remove_phone_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PersonPhone.objects.count(), 0)

    def test_remove_nonexistent_phone_from_person(self):
        """Test removing a phone that's not associated with the person"""
        data = {'phone_id': 999}  # Non-existent ID
        response = self.client.delete(self.remove_phone_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
