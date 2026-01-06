from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import UserProfile
from .serializers import UserProfileSerializer
from .r2_storage import R2Storage
import uuid
import os

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk CRUD User Profile dengan upload avatar ke Cloudflare R2
    
    Endpoints:
    - GET /api/profiles/ - List semua profiles
    - POST /api/profiles/ - Create profile baru
    - GET /api/profiles/{id}/ - Detail profile
    - PUT /api/profiles/{id}/ - Update profile
    - DELETE /api/profiles/{id}/ - Delete profile
    - POST /api/profiles/{id}/upload_avatar/ - Upload avatar
    - DELETE /api/profiles/{id}/delete_avatar/ - Delete avatar
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy untuk hapus avatar dari R2 saat delete profile"""
        profile = self.get_object()
        
        # Hapus avatar dari R2 jika ada
        if profile.avatar_filename:
            r2 = R2Storage()
            r2.delete_file(profile.avatar_filename)
        
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def upload_avatar(self, request, pk=None):
        """
        Upload avatar untuk user profile
        
        Request:
        - multipart/form-data
        - Field: 'avatar' (file)
        
        Response:
        {
            "success": true,
            "message": "Avatar uploaded successfully",
            "profile": {...},
            "avatar_url": "https://assets.senbi.online/xxx.jpg"
        }
        """
        profile = self.get_object()
        
        if 'avatar' not in request.FILES:
            return Response({
                'success': False,
                'error': 'No avatar file provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        avatar_file = request.FILES['avatar']
        
        # Validasi file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if avatar_file.content_type not in allowed_types:
            return Response({
                'success': False,
                'error': f'Invalid file type. Allowed: {", ".join(allowed_types)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validasi file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if avatar_file.size > max_size:
            return Response({
                'success': False,
                'error': 'File too large. Maximum size is 5MB'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate unique filename
        ext = os.path.splitext(avatar_file.name)[1]
        filename = f"avatars/{uuid.uuid4()}{ext}"
        
        # Upload ke R2
        r2 = R2Storage()
        result = r2.upload_file(avatar_file, filename)
        
        if not result['success']:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Hapus avatar lama jika ada
        if profile.avatar_filename:
            r2.delete_file(profile.avatar_filename)
        
        # Update profile dengan filename baru
        profile.avatar_filename = filename
        profile.save()
        
        serializer = self.get_serializer(profile)
        
        return Response({
            'success': True,
            'message': 'Avatar uploaded successfully',
            'profile': serializer.data,
            'avatar_url': result['url']
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def delete_avatar(self, request, pk=None):
        """
        Delete avatar dari user profile
        
        Response:
        {
            "success": true,
            "message": "Avatar deleted successfully"
        }
        """
        profile = self.get_object()
        
        if not profile.avatar_filename:
            return Response({
                'success': False,
                'error': 'No avatar to delete'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete dari R2
        r2 = R2Storage()
        result = r2.delete_file(profile.avatar_filename)
        
        if not result['success']:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Clear filename di database
        profile.avatar_filename = None
        profile.save()
        
        serializer = self.get_serializer(profile)
        
        return Response({
            'success': True,
            'message': 'Avatar deleted successfully',
            'profile': serializer.data
        }, status=status.HTTP_200_OK)
