from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('jobs/apply/', views.JobApplicationCreateView.as_view(), name='job-apply'),
    path('jobs/my-applications/', views.UserApplicationsListView.as_view(), name='my-applications'),
    path('jobs/<int:job_id>/check-application/', views.CheckApplicationStatusView.as_view(), name='check-application'),
    path('jobs/search-suggestions/', views.job_search_suggestions, name='job-search-suggestions'),
]