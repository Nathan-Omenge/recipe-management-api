from django.urls import path
from .views import register, login, logout, UserProfileView

urlpatterns = [
    path('api/auth/register/', register, name='register'),
    path('api/auth/login/', login, name='login'),
    path('api/auth/logout/', logout, name='logout'),
    path('api/auth/profile/', UserProfileView.as_view(), name='profile'),
]