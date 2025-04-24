from django.db import models
from django.db.models.functions import Now

from address.models import Address

class Person(models.Model):
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, blank=True)
    birthday = models.DateField(null=True, blank=True)
    first_contact = models.DateField(db_default=Now(), blank=True)
    addresses = models.ManyToManyField(Address, through="PersonAddress")

    class Meta:
        verbose_name_plural = "People"
        ordering = ["name", "first_contact"]

    def __str__(self):
        return self.name

class PersonAddress(models.Model):
    """
    PersonAddress is a through model for the many-to-many relationship between Person and Address.

    It's a separate model because we want to allow associating a label with the address.
    """
    label = models.CharField(max_length=255, default="Home")
    person = models.ForeignKey("person.person", on_delete=models.CASCADE)
    address = models.ForeignKey("address.address", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["person", "address"]
        verbose_name_plural = "Person addresses"

    def __str__(self):
        return f"{self.person.name}'s {self.label} address"

class PersonPhone(models.Model):
    """
    PersonPhone associates a labeled phone number with a person.
    """
    label = models.CharField(max_length=255, default="Mobile")
    person = models.ForeignKey("person.person", on_delete=models.CASCADE)
    # TODO: add phonenumbers package for better phone number handling
    phone = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["person", "phone"]
        verbose_name_plural = "Person phone numbers"

    def __str__(self):
        return f"{self.person.name}'s {self.label} phone number"
