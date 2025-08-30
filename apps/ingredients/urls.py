from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
