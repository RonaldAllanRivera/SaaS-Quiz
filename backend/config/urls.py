from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/lessons/', include('lessons.urls')),
    path('api/v1/quizzes/', include('quizzes.urls')),
    path('api/v1/reports/', include('reports.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

# Only for development:
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
