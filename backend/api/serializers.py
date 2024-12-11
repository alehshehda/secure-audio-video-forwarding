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
            'file_type': {'read_only': True},
            'uploaded_at': {'read_only': True}
        }
        

