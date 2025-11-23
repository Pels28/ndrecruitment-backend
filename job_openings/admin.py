# from django.contrib import admin
# from .models import Job, JobApplication

# @admin.register(Job)
# class JobAdmin(admin.ModelAdmin):
#     list_display = ['title', 'company', 'location', 'job_type', 'is_active', 'created_at']
#     list_filter = ['job_type', 'is_active', 'created_at']
#     search_fields = ['title', 'company', 'location']
#     list_editable = ['is_active']

# @admin.register(JobApplication)
# class JobApplicationAdmin(admin.ModelAdmin):
#     list_display = ['applicant', 'job', 'status', 'applied_at']
#     list_filter = ['status', 'applied_at', 'job__company']
#     search_fields = ['applicant__email', 'job__title', 'job__company']
#     readonly_fields = ['applied_at', 'updated_at']

# jobs/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.conf import settings
from .models import Job, JobApplication

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'is_active', 'created_at']
    list_filter = ['job_type', 'is_active', 'created_at']
    search_fields = ['title', 'company', 'location']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'applicant_name', 
        'applicant_email_link', 
        'job_title', 
        'company', 
        'status', 
        'download_resume',
        'applied_at'
    ]
    list_filter = ['status', 'applied_at', 'job__company', 'job__job_type']
    search_fields = [
        'applicant__email', 
        'applicant__first_name', 
        'applicant__last_name',
        'job__title', 
        'job__company'
    ]
    readonly_fields = [
        'applicant', 
        'job', 
        'applied_at', 
        'updated_at',
        'resume_preview',
        'view_cover_letter'
    ]
    list_editable = ['status']
    date_hierarchy = 'applied_at'
    
    fieldsets = (
        ('Application Info', {
            'fields': ('applicant', 'job', 'status', 'applied_at', 'updated_at')
        }),
        ('Resume & Documents', {
            'fields': ('resume', 'resume_preview', 'view_cover_letter',)
        }),
        ('Additional Information', {
            'fields': ('years_of_experience', 'linkedin_url', 'portfolio_url')
        }),
    )

    def applicant_name(self, obj):
        """Display applicant's full name"""
        return obj.applicant.get_full_name() or obj.applicant.username
    applicant_name.short_description = 'Applicant'
    applicant_name.admin_order_field = 'applicant__first_name'

    def applicant_email_link(self, obj):
        """Display clickable email link"""
        email = obj.applicant.email
        return format_html(
            '<a href="mailto:{}">{}</a>',
            email,
            email
        )
    applicant_email_link.short_description = 'Email'
    applicant_email_link.admin_order_field = 'applicant__email'

    def job_title(self, obj):
        """Display job title"""
        return obj.job.title
    job_title.short_description = 'Job Title'
    job_title.admin_order_field = 'job__title'

    def company(self, obj):
        """Display company name"""
        return obj.job.company
    company.short_description = 'Company'
    company.admin_order_field = 'job__company'

    def download_resume(self, obj):
        """Add download button for resume"""
        if obj.resume:
            # Get the raw Cloudinary URL
            resume_url = str(obj.resume.url)
            
            # If it's already a full URL, use it directly
            # Just add fl_attachment parameter for download
            if '?' in resume_url:
                download_url = f"{resume_url}&fl_attachment"
            else:
                download_url = f"{resume_url}?fl_attachment"
            
            return format_html(
                '<a href="{}" target="_blank" class="button" style="'
                'background-color: #417690; '
                'color: white; '
                'padding: 5px 10px; '
                'text-decoration: none; '
                'border-radius: 4px; '
                'display: inline-block;'
                '">📄 Download Resume</a>',
                download_url
            )
        return format_html('<span style="color: #999;">No resume</span>')
    download_resume.short_description = 'Resume'

    def resume_preview(self, obj):
        """Show resume with download and preview links in detail view"""
        if obj.resume:
            # Get the base Cloudinary URL
            resume_url = str(obj.resume.url)
            
            # Create download URL by adding fl_attachment parameter
            if '?' in resume_url:
                download_url = f"{resume_url}&fl_attachment"
            else:
                download_url = f"{resume_url}?fl_attachment"
            
            filename = obj.resume.name.split('/')[-1]
            
            return format_html(
                '<div style="margin: 10px 0;">'
                '<p><strong>File:</strong> {}</p>'
                '<p><strong>URL:</strong> <a href="{}" target="_blank">{}</a></p>'
                '<a href="{}" target="_blank" class="button" style="'
                'background-color: #417690; '
                'color: white; '
                'padding: 8px 15px; '
                'text-decoration: none; '
                'border-radius: 4px; '
                'display: inline-block; '
                'margin-right: 10px;'
                '">📄 Download Resume</a>'
                '<a href="{}" target="_blank" class="button" style="'
                'background-color: #52a952; '
                'color: white; '
                'padding: 8px 15px; '
                'text-decoration: none; '
                'border-radius: 4px; '
                'display: inline-block;'
                '">👁️ View in Browser</a>'
                '</div>',
                filename,
                resume_url,
                resume_url[:80] + '...' if len(resume_url) > 80 else resume_url,
                download_url,
                resume_url
            )
        return format_html('<span style="color: #999;">No resume uploaded</span>')
    resume_preview.short_description = 'Resume File'

    def view_cover_letter(self, obj):
        """Display cover letter in a readable format"""
        if obj.cover_letter:
            return format_html(
                '<div style="'
                'background-color: #f9f9f9; '
                'border: 1px solid #ddd; '
                'border-radius: 4px; '
                'padding: 15px; '
                'max-width: 800px; '
                'white-space: pre-wrap; '
                'font-family: Arial, sans-serif; '
                'line-height: 1.6;'
                '">{}</div>',
                obj.cover_letter
            )
        return format_html('<span style="color: #999;">No cover letter provided</span>')
    view_cover_letter.short_description = 'Cover Letter'

    def get_queryset(self, request):
        """Optimize queries with select_related"""
        queryset = super().get_queryset(request)
        return queryset.select_related('applicant', 'job')

    actions = ['mark_as_reviewed', 'mark_as_shortlisted', 'mark_as_rejected']

    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(status='reviewed')
        self.message_user(request, f'{updated} applications marked as reviewed.')
    mark_as_reviewed.short_description = 'Mark selected as Reviewed'

    def mark_as_shortlisted(self, request, queryset):
        updated = queryset.update(status='shortlisted')
        self.message_user(request, f'{updated} applications marked as shortlisted.')
    mark_as_shortlisted.short_description = 'Mark selected as Shortlisted'

    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} applications marked as rejected.')
    mark_as_rejected.short_description = 'Mark selected as Rejected'