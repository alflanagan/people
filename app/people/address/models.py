from django.db import models

class Address(models.Model):
    """An address of a person, organization, or place.

    Currently US only.

    Person, at least, will have a many-to-many relationship to Address. It should be defined in the Person model, as
    that is considered the 'primary' model.
    """

    label = models.CharField(max_length=255)
    first_line = models.CharField(max_length=255)
    second_line = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    # make this a ChoiceField?
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=10) # ZIP: 5 digits + dash + 4 digits

    class Meta:
        verbose_name_plural = "Addresses"
