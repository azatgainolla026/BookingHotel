from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mainapp.api_urls')),

    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-ui'),
    # JWT
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
