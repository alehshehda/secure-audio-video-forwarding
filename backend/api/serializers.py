from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserFiles


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFiles
        fields = ['id', 'user', 'file', 'uploaded_at', 'file_type']
        extra_kwargs = {
            'user': {'read_only': True},
            'file': {'required': True},
        }

    def create(self, validated_data):
        file = validated_data.get('file')  # Get the uploaded file
        user = validated_data.get('user')  # Get the user

        # Handle file_type automatically (based on the file MIME type)
        if file:
            file_type = file.content_type  # Get the MIME type of the file
            validated_data['file_type'] = file_type

        # Create the UserFiles instance
        user_file = UserFiles.objects.create(**validated_data)

        # Handle saving of the file
        user_file.file.save(file.name, file, save=True)

        return user_file
