from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .farmer.views import FarmerViewSet as farmer_api
from .location.views import CityViewSet as city_api
from .location.views import StateViewSet as state_api
from .rural_property.views import PlantationViewSet as plantation_api
from .rural_property.views import RuralPropertyViewSet as rural_property_api

router = DefaultRouter()

# locations
router.register('estados', state_api, basename='estados')
router.register('cidades', city_api, basename='cidades')
# farmers
router.register('proprietarios-rurais', farmer_api, basename='proprietarios-rurais')
# rural_property
router.register('propriedades-rurais', rural_property_api, basename='propriedades-rurais')
router.register('areas-plantadas', plantation_api, basename='areas-plantadas')

urlpatterns = [
    path('', include('backend.core.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
