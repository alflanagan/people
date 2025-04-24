from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from person.models import Person, PersonAddress, PersonPhone
from address.models import Address
import datetime

class PersonViewSetTests(APITestCase):
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

        # Create person-address relationship
        PersonAddress.objects.create(
            person=self.person,
            address=self.address,
            label="Home"
        )

        # Create a phone number for the person
        self.phone = PersonPhone.objects.create(
            person=self.person,
            label="Mobile",
            phone="555-123-4567"
        )

        # API endpoints
        self.list_url = reverse('person-list')
        self.detail_url = reverse('person-detail', kwargs={'pk': self.person.id})

    def test_get_person_list(self):
        """Test retrieving a list of persons"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_person_detail(self):
        """Test retrieving a single person"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')
        self.assertEqual(response.data['nickname'], 'Johnny')

    def test_create_person(self):
        """Test creating a new person"""
        data = {
            'name': 'Jane Smith',
            'nickname': 'Janie',
            'birthday': '1995-05-15',
            'first_contact': datetime.date.today().isoformat()
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 2)
        self.assertEqual(Person.objects.get(name='Jane Smith').nickname, 'Janie')

    def test_update_person(self):
        """Test updating an existing person"""
        data = {
            'name': 'John Doe',
            'nickname': 'JD',
            'birthday': '1990-01-01',
            'first_contact': self.person.first_contact.isoformat()
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.person.refresh_from_db()
        self.assertEqual(self.person.nickname, 'JD')

    def test_partial_update_person(self):
        """Test partially updating a person"""
        data = {'nickname': 'JD'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.person.refresh_from_db()
        self.assertEqual(self.person.nickname, 'JD')

    def test_delete_person(self):
        """Test deleting a person"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)

    def test_filter_person_by_name(self):
        """Test filtering persons by name"""
        # Create another person for testing filters
        Person.objects.create(
            name="Alice Johnson",
            first_contact=datetime.date.today()
        )

        url = f"{self.list_url}?name=John"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'John Doe')

    def test_filter_person_by_birthday(self):
        """Test filtering persons by birthday"""
        # Create another person with different birthday
        Person.objects.create(
            name="Alice Johnson",
            birthday=datetime.date(1985, 5, 10),
            first_contact=datetime.date.today()
        )

        url = f"{self.list_url}?birthday=1990-01-01"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'John Doe')
