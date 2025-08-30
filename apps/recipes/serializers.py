from rest_framework import serializers
from .models import Recipe, RecipeIngredient
from apps.categories.serializers import CategorySerializer
from apps.ingredients.serializers import IngredientSerializer

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'ingredient_name', 'quantity', 'unit', 'notes']
        read_only_fields = ['id']

class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit', 'notes']

class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    total_time = serializers.ReadOnlyField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'user', 'category', 'category_name', 'name', 'description', 
            'instructions', 'prep_time', 'cook_time', 'total_time', 'servings', 
            'difficulty', 'created_at', 'updated_at', 'recipe_ingredients'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(many=True, write_only=True)
    
    class Meta:
        model = Recipe
        fields = [
            'category', 'name', 'description', 'instructions', 
            'prep_time', 'cook_time', 'servings', 'difficulty', 'ingredients'
        ]
    
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient_data)
        
        return recipe

class RecipeListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    total_time = serializers.ReadOnlyField()
    ingredient_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'user', 'category_name', 'name', 'description', 
            'prep_time', 'cook_time', 'total_time', 'servings', 
            'difficulty', 'created_at', 'ingredient_count'
        ]
    
    def get_ingredient_count(self, obj):
        return obj.recipe_ingredients.count()