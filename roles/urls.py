from django.urls import path
from .views import RoleViewSet

role_list = RoleViewSet.as_view({'get':'list','post':'create'})
role_detail = RoleViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'})

urlpatterns=[path('organizations/<int:org_pk>/roles/', role_list, name='role-list'), path('organizations/<int:org_pk>/roles/<int:pk>/', role_detail, name='role-detail')]
