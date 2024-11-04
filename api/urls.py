from django.urls import path
from .views import ClientListCreateView, ClientDetailView, ProjectCreateView, UserProjectsListView

urlpatterns = [
    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('projects/', ProjectCreateView.as_view(), name='project-create'),
    path('user/projects/', UserProjectsListView.as_view(), name='user-projects'),
]
