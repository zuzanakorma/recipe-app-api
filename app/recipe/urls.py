"""URLs mapping for recipe APIs"""

from django.db import router
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
# will create new endpoint api/recipes
# autogenerated urls , viewset = get, post, delete, patch...
router.register("recipes", views.RecipeViewsSet)
router.register("tags", views.TagViewSet)
router.register("ingredients", views.IngredientViewSet)

app_name = "recipe"

urlpatterns = [path("", include(router.urls))]
