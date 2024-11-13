from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import ProtectedView, LoginView, LogoutView, CustomRefreshTokenView

urlpatterns = [
    
    path('dashboard/', ProtectedView.as_view(), name='user_dashboard'),
    path('register/', views.user_registration, name='register'),
    path('logout-that-login/', auth_views.logout_then_login, name='logout-than-login'),
  
  
  
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/protected/', ProtectedView.as_view(), name='protected'),
    path('api/token/refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    
    
]
