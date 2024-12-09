from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, UserFilesSerializer
from .models import Video
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    
class UploadVideoView(APIView):
    serializer_class = UserFilesSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = UserFilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
class VideoListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        videos = Video.objects.filter(user=request.user)
        serializer = UserFilesSerializer(videos, many=True)
        return Response(serializer.data)
            

class VideoDownloadView(APIView):     
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk, user=request.user)
        response = Response()
        response['Content-Disposition'] = f'attachment; filename="{video.file.name}"'
        response['X-Accel-Redirect'] = f'/media/{video.file.name}'
        return response



class VideoDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        video = get_object_or_404(Video, pk=pk, user=request.user)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


            

