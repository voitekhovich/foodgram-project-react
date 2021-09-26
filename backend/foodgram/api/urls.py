from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
