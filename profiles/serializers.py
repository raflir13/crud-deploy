from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ReadOnlyField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'bio', 'avatar_filename', 'avatar_url', 'created_at', 'updated_at']
        read_only_fields = ['avatar_filename', 'created_at', 'updated_at']
