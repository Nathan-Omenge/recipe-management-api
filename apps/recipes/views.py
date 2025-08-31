from rest_framework import viewsets, permissions, filters, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
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
    Users can only see and manage their own recipes.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description', 'instructions']
    filterset_fields = ['category', 'difficulty']  # Removed 'user' since we filter by user automatically
    ordering_fields = ['created_at', 'prep_time', 'cook_time', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Only return recipes owned by the current user
        return Recipe.objects.filter(user=self.request.user).select_related('user', 'category').prefetch_related('recipe_ingredients__ingredient')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializer
        elif self.action == 'list':
            return RecipeListSerializer
        return RecipeSerializer
    
    def perform_create(self, serializer):
        # Automatically set the user when creating a recipe
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_recipes(self, request):
        """Get current user's recipes (same as list, but explicit endpoint)"""
        recipes = self.get_queryset()
        page = self.paginate_queryset(recipes)
        if page is not None:
            serializer = RecipeListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = RecipeListSerializer(recipes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post', 'delete'])
    def ingredients(self, request, pk=None):
        """Add or remove ingredients from recipe"""
        recipe = self.get_object()  # get_object() already checks ownership via queryset filtering
        
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
        """Search recipes by ingredient name (within user's own recipes)"""
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