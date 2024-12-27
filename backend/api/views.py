from django.http import FileResponse
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
import uuid
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserFilesSerializer
from .models import UserFiles


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UploadFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the file exists in the request
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        # Create the directory path based on the user ID and file extension
        user_directory = os.path.join(settings.MEDIA_ROOT, str(request.user.id))
        file_extension = file.name.split('.')[-1]  # Get the file extension
        file_directory = os.path.join(user_directory, file_extension)

        # Ensure the directory exists
        os.makedirs(file_directory, exist_ok=True)

        try:
            # Instead of manually writing the file, let Django handle the file upload
            encrypted_file_int = UserFiles(user=request.user)
            encrypted_file_int.file = file  # Let Django handle the file saving
            encrypted_file_int.save()  # Let Django save the file and handle the filename

        except Exception as e:
            return Response({"error": f"Failed to save file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return the serialized response
        serializer = UserFilesSerializer(encrypted_file_int)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FilesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_files = UserFiles.objects.filter(user=request.user)
        serializer = UserFilesSerializer(user_files, many=True)
        return Response(serializer.data)


class FilesDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Retrieve the file object for the authenticated user
        user_files = get_object_or_404(UserFiles, pk=pk, user=request.user)

        # Get the full path to the file from the FileField (includes MEDIA_ROOT)
        file_path = user_files.file.path

        # Extract the file name (just the filename, not the full path)
        file_name = os.path.basename(file_path)

        try:
            # Open the file and return it as a streamed response
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)

        except FileNotFoundError:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FilesDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        # Retrieve the file object for the authenticated user
        user_files = get_object_or_404(UserFiles, pk=pk, user=request.user)
        file_path = user_files.file.path  # This is already the full path to the file

        # Log for debugging purposes
        print(f"Attempting to delete file at {file_path}")

        try:
            if os.path.exists(file_path):
                os.remove(file_path)  # Delete the file from the file system
                print(f"File {file_path} deleted successfully.")
            else:
                print(f"File not found at {file_path}")

            # Now delete the file record from the database
            user_files.delete()

        except Exception as e:
            print(f"Error deleting file: {e}")
            return Response({"error": "Cannot delete file"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "File deleted"}, status=status.HTTP_204_NO_CONTENT)


