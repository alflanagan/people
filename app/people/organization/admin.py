from django.contrib import admin

from .models import Organization, OrganizationPerson

class OrganizationPersonInline(admin.TabularInline):
        model = OrganizationPerson

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    inlines = [OrganizationPersonInline]
