from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import ProtectedView, LoginView, LogoutView, CustomRefreshTokenView, LoginPageView

urlpatterns = [
    
    path('dashboard/', ProtectedView.as_view(), name='user_dashboard'),
    path('register/', views.user_registration, name='register'),
    path('logout-that-login/', auth_views.logout_then_login, name='logout-than-login'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('api/token/refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('', views.dashboard, name='dashboard'),
    
    
]
