from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from cloudinary.models import CloudinaryField

User = get_user_model()

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    requirements = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company}"

    @property
    def salary_range(self):
        if self.salary_min and self.salary_max:
            return f"${self.salary_min:,.0f} - ${self.salary_max:,.0f}"
        elif self.salary_min:
            return f"From ${self.salary_min:,.0f}"
        elif self.salary_max:
            return f"Up to ${self.salary_max:,.0f}"
        return "Salary not specified"

    @property
    def posted_date(self):
        now = timezone.now()
        diff = now - self.created_at
    
    # Handle negative time differences
        if diff.total_seconds() < 0:
            return "Recently"
    
        seconds = diff.total_seconds()
    
        if seconds < 60:  # Less than 1 minute
            return "Just now"
        elif seconds < 3600:  # Less than 1 hour
            minutes = int(seconds // 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:  # Less than 1 day
            hours = int(seconds // 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:  # Less than 1 week
            days = int(seconds // 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif seconds < 2592000:  # Less than 1 month (30 days)
            weeks = int(seconds // 604800)
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        elif seconds < 31536000:  # Less than 1 year
            months = int(seconds // 2592000)
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = int(seconds // 31536000)
            return f"{years} year{'s' if years != 1 else ''} ago"

class JobApplication(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    resume = CloudinaryField(
        'document',
        folder='resumes/',
        resource_type='raw',  # Use 'raw' for documents
        blank=False,
        null=False
    )
    cover_letter = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['job', 'applicant']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.email} - {self.job.title}"