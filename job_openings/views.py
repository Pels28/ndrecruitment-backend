# from rest_framework import generics, status, filters
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from django_filters.rest_framework import DjangoFilterBackend
# from django.db.models import Q
# from django.shortcuts import get_object_or_404
# from .models import Job, JobApplication
# from .serializers import JobSerializer, JobApplicationSerializer, JobApplicationCreateSerializer
# from .pagination import JobPagination

# class JobListView(generics.ListAPIView):
#     serializer_class = JobSerializer
#     pagination_class = JobPagination
#     permission_classes = [AllowAny]  # Allow anyone to view jobs
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['title', 'company', 'description', 'requirements']
#     filterset_fields = ['job_type', 'location']
#     ordering_fields = ['created_at', 'salary_min', 'salary_max']
#     ordering = ['-created_at']

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context

#     def get_queryset(self):
#         queryset = Job.objects.filter(is_active=True)
        
#         # Custom filtering for salary range
#         min_salary = self.request.query_params.get('min_salary')
#         max_salary = self.request.query_params.get('max_salary')
        
#         if min_salary:
#             queryset = queryset.filter(salary_min__gte=min_salary)
#         if max_salary:
#             queryset = queryset.filter(salary_max__lte=max_salary)
            
#         return queryset

# class JobDetailView(generics.RetrieveAPIView):
#     queryset = Job.objects.filter(is_active=True)
#     serializer_class = JobSerializer
#     permission_classes = [AllowAny]  # Allow anyone to view job details

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context

# class JobApplicationCreateView(generics.CreateAPIView):
#     serializer_class = JobApplicationCreateSerializer
#     permission_classes = [IsAuthenticated]  # Only authenticated users can apply

#     def perform_create(self, serializer):
#         # Set the applicant to the current user when saving
#         serializer.save(applicant=self.request.user)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         # Check if user has already applied
#         job = serializer.validated_data['job']
#         if JobApplication.objects.filter(job=job, applicant=request.user).exists():
#             return Response(
#                 {"detail": "You have already applied to this job."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
        
#         return Response(
#             {
#                 "detail": "Application submitted successfully!",
#                 "application": serializer.data
#             },
#             status=status.HTTP_201_CREATED,
#             headers=headers
#         )

# class UserApplicationsListView(generics.ListAPIView):
#     serializer_class = JobApplicationSerializer
#     permission_classes = [IsAuthenticated]  # Only authenticated users can view their applications
#     pagination_class = JobPagination

#     def get_queryset(self):
#         return JobApplication.objects.filter(applicant=self.request.user)

# class CheckApplicationStatusView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]  # Only authenticated users can check application status

#     def retrieve(self, request, job_id):
#         job = get_object_or_404(Job, id=job_id, is_active=True)
        
#         try:
#             application = JobApplication.objects.get(job=job, applicant=request.user)
#             serializer = JobApplicationSerializer(application)
#             return Response({
#                 "has_applied": True,
#                 "application": serializer.data
#             })
#         except JobApplication.DoesNotExist:
#             return Response({
#                 "has_applied": False
#             })

# @api_view(['GET'])
# @permission_classes([AllowAny])  # Allow anyone to use search suggestions
# def job_search_suggestions(request):
#     query = request.GET.get('q', '')
    
#     if len(query) < 2:
#         return Response([])
    
#     # Search in titles and companies
#     title_suggestions = Job.objects.filter(
#         title__icontains=query, 
#         is_active=True
#     ).values_list('title', flat=True).distinct()[:5]
    
#     company_suggestions = Job.objects.filter(
#         company__icontains=query, 
#         is_active=True
#     ).values_list('company', flat=True).distinct()[:5]
    
#     location_suggestions = Job.objects.filter(
#         location__icontains=query, 
#         is_active=True
#     ).values_list('location', flat=True).distinct()[:5]
    
#     suggestions = list(title_suggestions) + list(company_suggestions) + list(location_suggestions)
    
#     return Response(suggestions[:10])


from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer, JobApplicationCreateSerializer
from .pagination import JobPagination

class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    pagination_class = JobPagination
    permission_classes = [AllowAny]  # Allow anyone to view jobs
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'company', 'description', 'requirements']
    filterset_fields = ['job_type', 'location']
    ordering_fields = ['created_at', 'salary_min', 'salary_max']
    ordering = ['-created_at']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)
        
        # Custom filtering for salary range
        min_salary = self.request.query_params.get('min_salary')
        max_salary = self.request.query_params.get('max_salary')
        
        if min_salary:
            queryset = queryset.filter(salary_min__gte=min_salary)
        if max_salary:
            queryset = queryset.filter(salary_max__lte=max_salary)
            
        return queryset

class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [AllowAny]  # Allow anyone to view job details
    lookup_field = 'slug'  # Use slug instead of ID
    lookup_url_kwarg = 'slug'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class JobApplicationCreateView(generics.CreateAPIView):
    serializer_class = JobApplicationCreateSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can apply

    def perform_create(self, serializer):
        # Set the applicant to the current user when saving
        serializer.save(applicant=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if user has already applied
        job = serializer.validated_data['job']
        if JobApplication.objects.filter(job=job, applicant=request.user).exists():
            return Response(
                {"detail": "You have already applied to this job."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {
                "detail": "Application submitted successfully!",
                "application": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class UserApplicationsListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can view their applications
    pagination_class = JobPagination

    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user)

class CheckApplicationStatusView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can check application status

    def retrieve(self, request, job_id):
        job = get_object_or_404(Job, id=job_id, is_active=True)
        
        try:
            application = JobApplication.objects.get(job=job, applicant=request.user)
            serializer = JobApplicationSerializer(application)
            return Response({
                "has_applied": True,
                "application": serializer.data
            })
        except JobApplication.DoesNotExist:
            return Response({
                "has_applied": False
            })

@api_view(['GET'])
@permission_classes([AllowAny])  # Allow anyone to use search suggestions
def job_search_suggestions(request):
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return Response([])
    
    # Search in titles and companies
    title_suggestions = Job.objects.filter(
        title__icontains=query, 
        is_active=True
    ).values_list('title', flat=True).distinct()[:5]
    
    company_suggestions = Job.objects.filter(
        company__icontains=query, 
        is_active=True
    ).values_list('company', flat=True).distinct()[:5]
    
    location_suggestions = Job.objects.filter(
        location__icontains=query, 
        is_active=True
    ).values_list('location', flat=True).distinct()[:5]
    
    suggestions = list(title_suggestions) + list(company_suggestions) + list(location_suggestions)
    
    return Response(suggestions[:10])