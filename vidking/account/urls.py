from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import ProtectedView, LoginView, LogoutView, CustomRefreshTokenView

urlpatterns = [
    
    path('register/', views.user_registration, name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/protected/', ProtectedView.as_view(), name='protected'),
    path('api/token/refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    
    
]
