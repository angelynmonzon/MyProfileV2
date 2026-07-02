import os
from django.core.files.storage import Storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import uuid


class SupabaseStorage(Storage):
    """
    Custom Django storage backend for Supabase Storage.
    Falls back to FileSystemStorage if Supabase is not configured or fails to initialize.
    """
    
    def __init__(self, bucket_name=None):
        self.bucket_name = bucket_name or getattr(settings, 'SUPABASE_STORAGE_BUCKET', 'images')
        self.supabase = None
        self.use_supabase = False
        self.fallback_storage = FileSystemStorage(location=getattr(settings, 'MEDIA_ROOT'))
        
        try:
            from supabase import create_client
            supabase_url = getattr(settings, 'SUPABASE_URL')
            supabase_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY')
            
            if supabase_url and supabase_key:
                self.supabase = create_client(supabase_url=supabase_url, supabase_key=supabase_key)
                self.use_supabase = True
        except Exception as e:
            # Fall back to default storage if Supabase fails to initialize
            print(f"Warning: Failed to initialize Supabase storage: {e}")
            self.use_supabase = False
    
    def _save(self, name, content):
        """
        Save file to Supabase Storage or fallback storage.
        """
        if not self.use_supabase:
            return self.fallback_storage._save(name, content)
        
        # Generate unique filename if needed
        if not name:
            name = f"{uuid.uuid4()}.{content.name.split('.')[-1]}"
        
        # Read file content
        content.seek(0)
        file_content = content.read()
        
        # Upload to Supabase
        try:
            result = self.supabase.storage.from_(self.bucket_name).upload(
                path=name,
                file=file_content,
                file_options={
                    'content-type': content.content_type if hasattr(content, 'content_type') else 'image/jpeg'
                }
            )
            return name
        except Exception as e:
            print(f"Warning: Failed to upload to Supabase, falling back to local storage: {e}")
            return self.fallback_storage._save(name, content)
    
    def url(self, name):
        """
        Get public URL for the file.
        """
        if not self.use_supabase:
            return self.fallback_storage.url(name)
        
        try:
            result = self.supabase.storage.from_(self.bucket_name).get_public_url(name)
            return result
        except Exception:
            # If public URL fails, try signed URL
            try:
                result = self.supabase.storage.from_(self.bucket_name).create_signed_url(
                    name,
                    expires_in=3600  # 1 hour
                )
                return result['signedURL']
            except Exception:
                # Fall back to local storage URL
                return self.fallback_storage.url(name)
    
    def exists(self, name):
        """
        Check if file exists in Supabase Storage.
        """
        if not self.use_supabase:
            return self.fallback_storage.exists(name)
        
        try:
            self.supabase.storage.from_(self.bucket_name).download(name)
            return True
        except Exception:
            return False
    
    def delete(self, name):
        """
        Delete file from Supabase Storage.
        """
        if not self.use_supabase:
            return self.fallback_storage.delete(name)
        
        try:
            self.supabase.storage.from_(self.bucket_name).remove([name])
        except Exception:
            pass
    
    def size(self, name):
        """
        Get file size from Supabase Storage.
        """
        if not self.use_supabase:
            return self.fallback_storage.size(name)
        
        try:
            result = self.supabase.storage.from_(self.bucket_name).get_metadata(name)
            return result.get('metadata', {}).get('size', 0)
        except Exception:
            return 0
    
    def get_available_name(self, name, max_length=None):
        """
        Generate a unique filename if the file already exists.
        """
        if self.exists(name):
            base, ext = os.path.splitext(name)
            name = f"{base}_{uuid.uuid4().hex[:8]}{ext}"
        return name
