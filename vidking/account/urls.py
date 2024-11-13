from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
<<<<<<< HEAD
from .views import ProtectedView, LoginView, LogoutView, CustomRefreshTokenView, LoginPageView, upload_success
from django.urls import path
from .views import upload_file
=======
from .views import ProtectedView, LoginView, LogoutView, CustomRefreshTokenView
>>>>>>> 5-adding-jwt

urlpatterns = [
    
    path('dashboard/', ProtectedView.as_view(), name='user_dashboard'),
    path('register/', views.user_registration, name='register'),
    path('logout-that-login/', auth_views.logout_then_login, name='logout-than-login'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/protected/', ProtectedView.as_view(), name='protected'),
    path('api/token/refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
<<<<<<< HEAD
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('upload/', upload_file, name='upload_file'),
    path('success/', upload_success, name='upload_success'),
=======

>>>>>>> 5-adding-jwt
    
    
]
