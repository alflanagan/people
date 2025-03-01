from django.contrib import admin
from .models import Person, PersonAddress, PersonPhone

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    plural_name = "People"
    list_select_related = True
    search_fields = ["name", "nickname"]

@admin.register(PersonAddress)
class PersonAddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(PersonPhone)
