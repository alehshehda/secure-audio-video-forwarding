from rest_framework import serializers
from account.models import UserFiles

class UserFilesSerializer(serializers.ModelSerializer):
    """
    Serializer for UserFiles model.

    This serializer handles the conversion of UserFiles model instances to and from JSON format.
    It includes the following fields:
    - id: The unique identifier for the user file.
    - user: The user who uploaded the file.
    - file: The file that was uploaded.
    - uploaded_at: The timestamp when the file was uploaded.
    - file_type: The type of the uploaded file.
    """
    
    
    class Meta:
        model = UserFiles
        fields = ['id', 'user', 'file', 'uploaded_at', 'file_type']
    