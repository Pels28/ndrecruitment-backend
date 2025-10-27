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


from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Job, JobApplication

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'is_active', 'created_at']
    list_filter = ['job_type', 'is_active', 'created_at']
    search_fields = ['title', 'company', 'location']
    list_editable = ['is_active']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at', 'resume_download_link']
    list_filter = ['status', 'applied_at', 'job__company']
    search_fields = ['applicant__email', 'job__title', 'job__company']
    readonly_fields = ['applied_at', 'updated_at', 'resume_display']
    
    def resume_download_link(self, obj):
        if obj.resume:
            # Get file info from Cloudinary
            public_id = obj.resume.public_id
            file_format = obj.resume.format or 'file'
            file_size = getattr(obj.resume, 'bytes', 0)
            
            # Format file size
            if file_size > 0:
                if file_size < 1024 * 1024:  # Less than 1MB
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
            else:
                size_str = "Unknown size"
            
            return format_html(
                '''
                <div style="display: flex; align-items: center; gap: 10px;">
                    <a href="{}" target="_blank" 
                       style="background-color: #007bff; color: white; padding: 4px 8px; text-decoration: none; border-radius: 4px; font-size: 12px;">
                        📥 Download
                    </a>
                    <span style="font-size: 11px; color: #666;">
                        {} • {}
                    </span>
                </div>
                ''',
                obj.resume.url,
                file_format.upper(),
                size_str
            )
        return format_html('<span style="color: #999;">No resume</span>')
    resume_download_link.short_description = 'Resume'
    
    def resume_display(self, obj):
        if obj.resume:
            # Get detailed file information
            public_id = obj.resume.public_id
            file_format = obj.resume.format or 'Unknown format'
            file_size = getattr(obj.resume, 'bytes', 0)
            
            # Format file size
            if file_size > 0:
                if file_size < 1024 * 1024:  # Less than 1MB
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
            else:
                size_str = "Unknown size"
            
            return format_html(
                '''
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; background-color: #f9f9f9;">
                    <h4 style="margin-top: 0;">Resume File</h4>
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
                        <a href="{}" target="_blank" 
                           style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                            📄 Download Resume
                        </a>
                        <div style="font-size: 14px;">
                            <div><strong>Format:</strong> {}</div>
                            <div><strong>Size:</strong> {}</div>
                        </div>
                    </div>
                    <div style="font-size: 12px; color: #666;">
                        <strong>Cloudinary ID:</strong> {}
                    </div>
                </div>
                ''',
                obj.resume.url,
                file_format.upper(),
                size_str,
                public_id
            )
        return format_html(
            '<div style="color: #dc3545; font-style: italic;">No resume file uploaded</div>'
        )
    resume_display.short_description = 'Resume File Details'
    
    fieldsets = (
        ('Application Information', {
            'fields': ('job', 'applicant', 'status')
        }),
        ('Resume & Documents', {
            'fields': ('resume_display', 'cover_letter', 'years_of_experience')
        }),
        ('Additional Information', {
            'fields': ('linkedin_url', 'portfolio_url')
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )