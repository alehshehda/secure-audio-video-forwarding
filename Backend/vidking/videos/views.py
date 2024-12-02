from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import UserFilesSerializer
from django.shortcuts import get_object_or_404


class UploadVideoView(APIView):
    
    """
    UploadVideoView handles the uploading of video files by authenticated users.
    Methods:
        post(request):
            Handles the POST request to upload a video file. Validates the incoming data using UserFilesSerializer.
            If the data is valid, saves the file associated with the authenticated user and returns the serialized data
            with a 201 Created status. If the data is invalid, returns the validation errors with a 400 Bad Request status.
    Attributes:
        permission_classes (list): Specifies that the view requires the user to be authenticated.
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = UserFilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoListView(APIView):
    
    """
    VideoListView is an API view that handles GET requests to retrieve a list of videos
    associated with the authenticated user.
    Attributes:
        permission_classes (list): A list of permission classes that the view requires. 
                                   In this case, the user must be authenticated.
    Methods:
        get(request):
            Handles GET requests to retrieve videos associated with the authenticated user.
            Filters the Video objects by the requesting user and serializes the data using
            UserFilesSerializer. Returns a Response object containing the serialized data.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        videos = Video.objects.filter(user=request.user)
        serializer = UserFilesSerializer(videos, many=True)
        return Response(serializer.data)

class VideoDownloadView(APIView): 
    
    """
    VideoDownloadView handles the download of video files for authenticated users.
    Methods:
        get(request, pk): Retrieves the video file associated with the given primary key (pk) 
                          and the authenticated user, and prepares it for download.
    Attributes:
        permission_classes (list): Specifies that the view requires the user to be authenticated.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk, user=request.user)
        response = Response()
        response['Content-Disposition'] = f'attachment; filename="{video.file.name}"'
        response['X-Accel-Redirect'] = f'/media/{video.file.name}'
        return response
            

