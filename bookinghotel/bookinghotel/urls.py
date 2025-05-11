from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # api
    path('api/', include('mainapp.api_urls')),
    # silk
    path('silk/', include('silk.urls', namespace='silk')),
    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-ui'),

]
