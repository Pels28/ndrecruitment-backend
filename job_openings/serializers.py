from rest_framework import serializers
from .models import Job, JobApplication
from django.contrib.auth import get_user_model

User = get_user_model()


class JobSerializer(serializers.ModelSerializer):
    salary_range = serializers.ReadOnlyField()
    posted_date = serializers.ReadOnlyField()
    has_applied = serializers.SerializerMethodField()
    slug = serializers.ReadOnlyField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'location', 'job_type', 
            'salary_range', 'description', 'requirements', 
            'is_active', 'created_at', 'posted_date', 'has_applied', 'slug'
        ]

    def get_has_applied(self, obj):
        request = self.context.get('request')
        # Check if request exists and user is authenticated
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return JobApplication.objects.filter(
                job=obj, 
                applicant=request.user
            ).exists()
        return False
    
class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company', read_only=True)
    job_slug = serializers.CharField(source='job.slug', read_only=True)
    applicant_name = serializers.CharField(source='applicant.get_full_name', read_only=True)
    applicant_email = serializers.CharField(source='applicant.email', read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'job_title', 'company_name', 'job_slug', 'applicant', 
            'applicant_name', 'applicant_email', 'resume', 'cover_letter',
            'years_of_experience', 'linkedin_url', 'portfolio_url',
            'status', 'applied_at'
        ]
        read_only_fields = ['applicant', 'status']

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            'job', 'resume', 'cover_letter', 'years_of_experience',
            'linkedin_url', 'portfolio_url'
        ]

    def validate(self, attrs):
        job = attrs.get('job')
        user = self.context['request'].user

        # Check if user has already applied to this job
        if JobApplication.objects.filter(job=job, applicant=user).exists():
            raise serializers.ValidationError("You have already applied to this job.")

        return attrs

    def create(self, validated_data):
        # Set the applicant to the current user
        validated_data['applicant'] = self.context['request'].user
        
        # Create and return the JobApplication instance
        return JobApplication.objects.create(**validated_data)