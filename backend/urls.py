from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .farmer.views import FarmerViewSet as farmer_api
from .location.views import CityViewSet as city_api
from .location.views import StateViewSet as state_api
from .rural_property.views import PlantationViewSet as plantation_api
from .rural_property.views import RuralPropertyViewSet as rural_property_api

router = DefaultRouter()

# locations
router.register('states', state_api, basename='states')
router.register('cities', city_api, basename='cities')
# farmers
router.register('farmers', farmer_api, basename='farmers')
# rural_property
router.register('rural-properties', rural_property_api, basename='rural-properties')
router.register('plantations', plantation_api, basename='plantations')

urlpatterns = [
    path('', include('backend.core.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', obtain_auth_token)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
