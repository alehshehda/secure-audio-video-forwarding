from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, UserFilesSerializer
from .models import UserFiles
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os



class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    
class UploadFilesView(APIView):
    serializer_class = UserFilesSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        file = request.FILES['file']
        print(file)
        user_file = UserFiles(user=request.user, file=file)
        user_file.save()

        serializer = UserFilesSerializer(user_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            
class FilesListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Получаем все UserFiles, связанные с текущим пользователем
        user_files = UserFiles.objects.filter(user=request.user)
        serializer = UserFilesSerializer(user_files, many=True)
        return Response(serializer.data)
            

class FilesDownloadView(APIView):     
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        user_files = get_object_or_404(UserFiles, pk=pk, user=request.user)
        serializer = UserFilesSerializer(user_files)
        return Response(serializer.data)



class FilesDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        user_files = get_object_or_404(UserFiles, pk=pk, user=request.user)
        file_path = user_files.file.path

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            return Response({"error": "Cannot delete file"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        user_files.delete()
        
        return Response({"message": "File deleted"}, status=status.HTTP_204_NO_CONTENT)
            

            

