from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey("address.address", on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    people = models.ManyToManyField("person.person", through="OrganizationPerson")

class OrganizationPerson(models.Model):
    """
    OrganizationPerson associates a person with an organization.
    """
    organization = models.ForeignKey("organization.organization", on_delete=models.CASCADE)
    person = models.ForeignKey("person.person", on_delete=models.CASCADE)
    # TODO: define lookup table for roles, which user can define
    role = models.CharField(max_length=255, default="Member")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("organization", "person")
