from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate
from .forms import UserRegistationForm
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserFileForm
from .models import UserFiles


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'dashboard': 'dashboard'})


class ProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print(f"User: {request.user}") 
        content = {'message': 'This is a protected endpoint!'}
        return Response(content)

class LoginPageView(TemplateView):
    template_name = 'registration/login.html'

    

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            response = JsonResponse({'message': 'Login successful!'})
            
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax'
            )

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            response = redirect('user_dashboard')
            return response
        else:
            return JsonResponse({'error': 'Invalid Credentials'}, status=401)

class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')  
        if refresh_token is None:
            return JsonResponse({"error": "Refresh token missing"}, status=401)
        
        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data['access']
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax'
            )
        return response
    
    
class LogoutView(APIView):
    def post(self, request):
        response = JsonResponse({'logout_message': 'You have successfuly logout!'})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response            

def user_registration(request):
    if request.method == 'POST':
        user_form = UserRegistationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistationForm()
    return render(request, 'account/register.html', {'user_form':user_form})
            
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            user_file = form.save(commit=False)  # Nie zapisuj jeszcze do bazy danych
            user_file.user = request.user  # Ustaw użytkownika na aktualnie zalogowanego
            user_file.save()  # Zapisz plik do bazy danych
            return redirect('upload_success')  # Przekieruj do strony sukcesu
    else:
        form = UserFileForm()

    return render(request, 'upload_file.html', {'form': form})

def upload_success(request):
    return render(request, 'upload_success.html')
