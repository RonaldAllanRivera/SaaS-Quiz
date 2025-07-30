import os
from pathlib import Path
import environ
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
# This will read the .env file in the backend/ directory
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ==== Site Info ====
SITE_NAME = os.getenv("SITE_NAME", "QuizNest")
SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ==== Security ====
SECRET_KEY = os.getenv("SECRET_KEY", "dev-fallback-secret")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.28'] + os.getenv("ALLOWED_HOSTS", "*").split(",")

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

# ==== Installed Apps ====
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required by allauth

    # 3rd Party
    'whitenoise.runserver_nostatic',  # Disable Django's static file handling in dev
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # Local
    'users',
    'lessons',
    'quizzes',
    'reports',
    'books',
]

# ==== Middleware ====
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add whitenoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', # allauth middleware
]

# ==== Media Files ====
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==== URLs & WSGI ====
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ==== Sites Framework ====
SITE_ID = 1



# ==== Authentication Backends ====
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# ==== Templates (needed for Admin) ====
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==== Database ====
if ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Prefer os.environ.get for flexibility here, then coerce to string
    db_url = os.environ.get('DATABASE_URL') or f'sqlite:///{BASE_DIR / "db.sqlite3"}'
    DATABASES = {
        'default': dj_database_url.config(default=db_url)
    }


# ==== Password Validators (Minimal) ====
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
]

# ==== Internationalization ====
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==== Static Files ====
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==== Default Primary Key ====
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==== Custom User Model ====
AUTH_USER_MODEL = "users.User"

# ==== Email Configuration ====
if ENVIRONMENT == 'production':
    # Production email settings from environment variables
    EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
    EMAIL_HOST = os.getenv('EMAIL_HOST', '')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@quiznest.com')
    SERVER_EMAIL = DEFAULT_FROM_EMAIL  # For error notifications
else:
    # Development email settings
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'noreply@quiznest.com'
DEFAULT_ADMIN_EMAIL = os.getenv("DEFAULT_ADMIN_EMAIL", "your-admin@email.com")

# ==== Third-Party API Keys ====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# ==== Authentication ====
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# ==== Django Allauth and dj-rest-auth ====
REST_AUTH = {
    'USE_JWT': False, # We are using Token Authentication
    'SESSION_LOGIN': True,
    'TOKEN_SERIALIZER': 'dj_rest_auth.serializers.TokenSerializer',
}

# allauth-specific settings
ACCOUNT_LOGIN_METHODS = {'email'}        # Use email for login
# Email verification settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True

# Set email verification based on environment
if ENVIRONMENT == 'production':
    # In production, require email verification
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    SOCIALACCOUNT_EMAIL_VERIFICATION = 'mandatory'
else:
    # In development, don't require email verification
    ACCOUNT_EMAIL_VERIFICATION = 'optional'
    SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional'

# Adapters for allauth and social authentication
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    },
    # Facebook provider has been removed - using Google only for authentication
}
