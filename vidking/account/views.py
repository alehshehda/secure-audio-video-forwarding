from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import UserRegistationForm
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            return Response({
                'access_token': access_token,
                'refresh_token': str(refresh)
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=401)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        content = {'message': 'This is a protected endpoint!', 'user': user.username}
        return Response(content)


class LogoutView(APIView):
    def post(self, request):
        # Просто возвращаем сообщение о выходе
        return Response({'message': 'You have successfully logged out!'})
   
   
class CustomRefreshTokenView(TokenRefreshView):
    pass

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
            
