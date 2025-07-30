from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from users.views import GoogleLogin


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API V1
    path('api/v1/users/', include('users.urls')),
    path('api/v1/lessons/', include('lessons.urls')),
    path('api/v1/quizzes/', include('quizzes.urls')),
    path('api/v1/reports/', include('reports.urls')),
    path('api/v1/books/', include('books.urls')),

    # Django Allauth URLs - Required for social authentication
    path('accounts/', include('allauth.urls')),  # This includes the account_signup URL
    
    # REST Auth
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # Social Authentication (Google only)
    path('api/v1/auth/google/', GoogleLogin.as_view(), name='google_login'),

    # Legacy auth, to be deprecated
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

# Only for development:
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
