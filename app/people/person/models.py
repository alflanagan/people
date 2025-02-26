from django.db import models
from django.db.models.functions import Now

class Person(models.Model):
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, blank=True)
    birthday = models.DateField(null=True, blank=True)
    first_contact = models.DateField(db_default=Now(), blank=True)


class PersonAddress(models.Model):
    label = models.CharField(max_length=255, default="Home")
    person = models.ForeignKey("person.person", on_delete=models.CASCADE)
    address = models.ForeignKey("address.address", on_delete=models.CASCADE)
