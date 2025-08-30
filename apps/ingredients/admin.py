from django.contrib import admin
from .models import Ingredient

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'default_unit', 'category', 'created_at']
    search_fields = ['name', 'category']
    list_filter = ['category']