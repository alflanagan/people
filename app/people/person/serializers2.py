from rest_framework import serializers
from .models import Person, PersonAddress, PersonPhone
from address.serializers import AddressSerializer

class PersonPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonPhone
        fields = ['id', 'label', 'phone', 'created']

class PersonAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = PersonAddress
        fields = ['id', 'label', 'address', 'created']

class PersonSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    phones = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['id', 'name', 'nickname', 'birthday', 'first_contact', 'addresses', 'phones']

    def get_phones(self, obj):
        person_phones = PersonPhone.objects.filter(person=obj)
        return PersonPhoneSerializer(person_phones, many=True).data
