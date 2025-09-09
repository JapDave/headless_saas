from django.urls import path
from .views import OrgUserViewSet

user_list = OrgUserViewSet.as_view({"get":"list","post":"create"})
user_detail = OrgUserViewSet.as_view({"get":"retrieve","put":"update","patch":"partial_update","delete":"destroy"})

urlpatterns = [
    path("organizations/<int:org_pk>/users/", user_list, name="user-list"),
    path("organizations/<int:org_pk>/users/<int:pk>/", user_detail, name="user-detail"),
]
