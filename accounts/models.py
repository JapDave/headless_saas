from django.db import models
from core.models import SoftDeleteModel


class Account(SoftDeleteModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="created_accounts")
    def __str__(self): 
        return self.name

class Organization(SoftDeleteModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="organizations")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo_url = models.URLField(blank=True)
    def __str__(self): 
        return f"{self.name}"
