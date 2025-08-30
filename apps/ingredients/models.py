from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=150, unique=True)
    default_unit = models.CharField(max_length=20, default='grams')
    category = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name