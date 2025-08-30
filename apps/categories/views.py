from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing categories.
    Only administrators can create/edit categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]  # Categories are public
    
    @action(detail=True, methods=['get'])
    def recipes(self, request, pk=None):
        """Get all recipes in this category"""
        category = self.get_object()
        recipes = category.recipes.all()
        from apps.recipes.serializers import RecipeListSerializer
        serializer = RecipeListSerializer(recipes, many=True)
        return Response(serializer.data)