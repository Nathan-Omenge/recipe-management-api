from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Recipe, RecipeIngredient
from .serializers import (
    RecipeSerializer, RecipeCreateSerializer, RecipeListSerializer,
    RecipeIngredientSerializer
)

class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing recipes.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description', 'instructions']
    filterset_fields = ['category', 'difficulty', 'user']
    ordering_fields = ['created_at', 'prep_time', 'cook_time', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Recipe.objects.select_related('user', 'category').prefetch_related('recipe_ingredients__ingredient')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializer
        elif self.action == 'list':
            return RecipeListSerializer
        return RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def my_recipes(self, request):
        """Get current user's recipes"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        recipes = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(recipes)
        if page is not None:
            serializer = RecipeListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = RecipeListSerializer(recipes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post', 'delete'])
    def ingredients(self, request, pk=None):
        """Add or remove ingredients from recipe"""
        recipe = self.get_object()
        
        # Check if user owns the recipe
        if recipe.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        if request.method == 'POST':
            serializer = RecipeIngredientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(recipe=recipe)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            ingredient_id = request.data.get('ingredient_id')
            try:
                recipe_ingredient = RecipeIngredient.objects.get(
                    recipe=recipe, 
                    ingredient_id=ingredient_id
                )
                recipe_ingredient.delete()
                return Response({'message': 'Ingredient removed'}, status=status.HTTP_204_NO_CONTENT)
            except RecipeIngredient.DoesNotExist:
                return Response({'error': 'Ingredient not found in recipe'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def search_by_ingredient(self, request):
        """Search recipes by ingredient name"""
        ingredient_name = request.query_params.get('ingredient', '')
        if not ingredient_name:
            return Response({'error': 'ingredient parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        recipes = self.get_queryset().filter(
            recipe_ingredients__ingredient__name__icontains=ingredient_name
        ).distinct()
        
        page = self.paginate_queryset(recipes)
        if page is not None:
            serializer = RecipeListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = RecipeListSerializer(recipes, many=True)
        return Response(serializer.data)


# Custom permission class
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the recipe.
        return obj.user == request.user