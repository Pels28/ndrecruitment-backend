

# settings.py
from pathlib import Path
from datetime import timedelta
from os import getenv
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# Fix the DEBUG setting - Render sets RENDER environment variable
DEBUG = getenv("IS_DEVELOPMENT", "False").lower() == "true"

# Proper ALLOWED_HOSTS for Render
ALLOWED_HOSTS = [
    'ndrecruitment-backend.onrender.com',
    'localhost',
    '127.0.0.1',
]

# Add Render's external hostname if available
RENDER_EXTERNAL_HOSTNAME = getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition
AUTH_USER_MODEL = 'base.CustomUser'

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'job_openings',
    'django_filters',
    'blogs',
    'cloudinary',
    'cloudinary_storage',
]

# Updated middleware with WhiteNoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nd_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nd_backend.wsgi.application'

# Database
DATABASE_URL = getenv("DATABASE_URL")
DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Only set STATIC_ROOT in production
if not DEBUG:
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    # Enable WhiteNoise compression and caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files - use Cloudinary in production
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': getenv("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': getenv("CLOUDINARY_API_KEY"),
    'API_SECRET': getenv("CLOUDINARY_API_SECRET"),
    'SECURE': True,  # Force HTTPS
}

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ) 
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=7),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=30),
}

JAZZMIN_SETTINGS = {
    # Title of the window
    "site_title": "North Devon Admin",

    # Title on the login screen
    "site_header": "North Devon",

    # Title on the brand
    "site_brand": "North Devon",

    # Logo to use for your site, must be present in static files
    "site_logo": "images/logo.png",

    # Logo to use for login form
    "login_logo": "images/logo.png",

    # Logo for login form in dark themes
    "login_logo_dark": None,

    # CSS classes that are applied to the logo
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site
    "site_icon": "images/favicon.ico",

    # Welcome text on the login screen
    "welcome_sign": "Welcome to North Devon Admin Portal",

    # Copyright on the footer
    "copyright": " North Devon - BPX Innovations Ltd",

    # List of model admins to search from the search bar
    "search_model": ["base.CustomUser", "job_openings.Job", "blogs.Post"],

    # Field name on user model that contains avatar
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [
        # Home link
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        
        # View site link
        {"name": "View Site", "url": "https://ndrecruitment.vercel.app/", "new_window": True},
        
        # Quick links to main models
        # {"model": "base.CustomUser"},
        # {"model": "job_openings.Job"},
        # {"model": "blogs.Post"},
        {"app": "job_openings"},
        {"app": "blogs"},
        {"app": "base"}
    ],

    #############
    # User Menu #
    #############

    # Additional links in the user menu on the top right
    "usermenu_links": [
        {"name": "View Site", "url": "https://ndrecruitment.vercel.app/", "new_window": True},
        {"model": "base.CustomUser"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to auto expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu
    "hide_apps": [],

    # Hide these models when generating side menu
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of
    "order_with_respect_to": ["base", "job_openings", "blogs", "auth"],

    # Custom icons for side menu apps/models
    # Using Font Awesome 5 icons: https://fontawesome.com/v5/search?m=free
    "icons": {
        # Authentication & Authorization
        "auth": "fas fa-shield-alt",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        
        # Base (Users)
        "base": "fas fa-user-circle",
        "base.CustomUser": "fas fa-users",
        
        # Job Openings
        "job_openings": "fas fa-briefcase",
        "job_openings.Job": "fas fa-briefcase",
        "job_openings.JobApplication": "fas fa-file-alt",
        
        # Blogs
        "blogs": "fas fa-blog",
        "blogs.Author": "fas fa-user-edit",
        "blogs.Category": "fas fa-folder",
        "blogs.Post": "fas fa-newspaper",
        "blogs.Tag": "fas fa-tags",
    },
    
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts
    "custom_css": "admin/css/jazzmin_custom.css",
    "custom_js": None,
    
    # Whether to link font from fonts.googleapis.com
    "use_google_fonts_cdn": True,
    
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs
    # Options: single, horizontal_tabs, vertical_tabs, collapsible, carousel
    "changeform_format": "horizontal_tabs",
    
    # Override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "base.customuser": "collapsible",
        "auth.group": "vertical_tabs",
        "job_openings.job": "horizontal_tabs",
        "blogs.post": "horizontal_tabs",
    },
    
    # Add a language dropdown into the admin
    "language_chooser": False,
}

# Jazzmin UI Tweaks - Color Customization
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-white",
    "accent": "accent-orange",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-orange",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "lumen",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}

CORS_ALLOW_ALL_ORIGINS = True