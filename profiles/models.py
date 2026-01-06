from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar_filename = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def avatar_url(self):
        """Return full URL untuk avatar di Cloudflare R2"""
        if self.avatar_filename:
            from django.conf import settings
            return f"{settings.R2_PUBLIC_URL}/{self.avatar_filename}"
        return None