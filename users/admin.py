# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # What shows in list view
    list_display = ("username", "email", "organization", "status", "is_active", "is_staff")
    list_filter = ("status", "is_active", "is_staff", "organization")

    # Add our fields to the standard Django user sections
    fieldsets = (
        ("Authentication", {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("full_name", "email", "organization", "profile_image", "user_preferences")}),
        ("Status & permissions", {
            "fields": (
                "status",          # our domain status (label now: Account status)
                "is_active",       # Django's login flag (checkbox)
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {"fields": ("last_login", "date_joined", "deleted_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "organization", "status", "is_staff", "is_superuser"),
        }),
    )