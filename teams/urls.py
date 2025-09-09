from django.urls import path
from .views import TeamViewSet
team_list = TeamViewSet.as_view({'get':'list','post':'create'})
team_detail = TeamViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'})
urlpatterns=[path('organizations/<int:org_pk>/teams/', team_list, name='team-list'), path('organizations/<int:org_pk>/teams/<int:pk>/', team_detail, name='team-detail')]
