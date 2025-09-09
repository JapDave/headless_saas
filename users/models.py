# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import SoftDeleteModel

class User(AbstractUser, SoftDeleteModel):
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    organization = models.ForeignKey(
        "accounts.Organization", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="users"
    )
    # Remove if you decided to go pure RBAC; otherwise keep internal-only
    is_org_admin = models.BooleanField(default=False)

    STATUS_CHOICES = [("active","Active"),("inactive","Inactive"),("suspended","Suspended")]
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name="Account status",
        help_text="Domain-level status; Inactive/Suspended disables login."
    )
    profile_image = models.URLField(blank=True)
    user_preferences = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="created_users")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["organization","email"], name="uniq_email_per_org")]

    def __str__(self):
        return self.username or self.email

    def save(self, *args, **kwargs):
        # Keep Django's auth flag in lockstep with domain status
        self.is_active = (self.status == "active")
        super().save(*args, **kwargs)
