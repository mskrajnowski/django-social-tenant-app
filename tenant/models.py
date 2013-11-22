from django.db import models
from tenant_schemas.models import TenantMixin


class Tenant(TenantMixin):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, default="")

    allowed_emails = models.TextField(blank=True, default="")

    def is_email_allowed(self, email_address):
        email_address = email_address.lower()

        for pattern in self.allowed_emails.split(","):
            pattern = pattern.strip().lower()

            match = (email_address.endswith(pattern[1:])
                     if pattern.startswith("*")
                     else email_address == pattern)

            if match:
                return True

        return False

