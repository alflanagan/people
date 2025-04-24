from rest_framework import serializers
from .models import Person, PersonAddress, PersonPhone
from address.models import Address
from address.serializers import AddressSerializer

class PersonPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonPhone
        fields = ['id', 'phone', 'label']

class PersonAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = PersonAddress
        fields = ['id', 'label', 'address']

class PersonSerializer(serializers.ModelSerializer):
    addresses = PersonAddressSerializer(source='personaddress_set', many=True, read_only=True)
    phones = PersonPhoneSerializer(source='personphone_set', many=True, read_only=True)

    class Meta:
        model = Person
        fields = ['id', 'name', 'nickname', 'birthday', 'first_contact', 'addresses', 'phones']
