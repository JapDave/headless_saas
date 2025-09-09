from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, OrganizationViewSet

router = DefaultRouter(); router.register(r"accounts", AccountViewSet, basename="account")
org_list = OrganizationViewSet.as_view({"get":"list","post":"create"})
org_detail = OrganizationViewSet.as_view({"get":"retrieve","put":"update","patch":"partial_update","delete":"destroy"})

urlpatterns = [ path("", include(router.urls)),
    path("accounts/<int:account_pk>/organizations/", org_list, name="org-list"),
    path("accounts/<int:account_pk>/organizations/<int:pk>/", org_detail, name="org-detail"),
]
