from django.db import models
from core.models import SoftDeleteModel

class Role(SoftDeleteModel):
    organization = models.ForeignKey("accounts.Organization", null=True, blank=True, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_custom = models.BooleanField(default=True)
    permissions = models.JSONField(default=list, blank=True)
    
    class Meta: 
        unique_together = ("organization","name")


class UserRole(SoftDeleteModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")
    
    class Meta: 
        unique_together = ("user","role")
