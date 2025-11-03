from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry


# class NorthDevonAdminSite(AdminSite):
#     site_header = 'North Devon Administration'
#     site_title = 'North Devon Admin'
#     index_title = 'Dashboard'
    
#     def index(self, request, extra_context=None):
#         from base.models import CustomUser
#         from job_openings.models import Job, JobApplication
#         from blogs.models import Post
        
#         extra_context = extra_context or {}
#         extra_context['total_users'] = CustomUser.objects.count()
#         extra_context['total_jobs'] = Job.objects.filter(is_active=True).count()
#         extra_context['total_applications'] = JobApplication.objects.count()
#         extra_context['total_posts'] = Post.objects.count()
#         extra_context['admin_log'] = LogEntry.objects.select_related('user').order_by('-action_time')[:10]
        
#         return super().index(request, extra_context=extra_context)

# # Create instance
# admin_site = NorthDevonAdminSite(name='admin')

@admin.register(CustomUser)
class CustomAdminUser(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ['email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-date_joined',)
    
    # Fieldsets for EDITING existing users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fieldsets for ADDING new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2'),
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_staff', 'is_active'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')