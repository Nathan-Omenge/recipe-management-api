from django.contrib import admin
from .models import Recipe, RecipeIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'difficulty', 'prep_time', 'cook_time', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['category', 'difficulty', 'user']
    inlines = [RecipeIngredientInline]

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'quantity', 'unit']
    list_filter = ['unit']