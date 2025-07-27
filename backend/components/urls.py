from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComponentCategoryViewSet, ManufacturerViewSet, ComponentViewSet, ComponentPriceViewSet

router = DefaultRouter()
router.register('categories', ComponentCategoryViewSet)
router.register('manufacturers', ManufacturerViewSet)
router.register('components', ComponentViewSet)
router.register('prices', ComponentPriceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]