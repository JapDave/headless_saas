from django.db import models
from core.models import SoftDeleteModel

class Team(SoftDeleteModel):
    organization = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    configurations = models.JSONField(default=dict, blank=True)
    def __str__(self): return self.name
