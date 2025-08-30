from rest_framework import serializers
from .models import Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'default_unit', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']
