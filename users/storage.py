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
                print(f"[Supabase] Storage initialized OK, bucket='{self.bucket_name}'")
            else:
                print("[Supabase] Credentials not set, using local storage")
        except Exception as e:
            print(f"[Supabase] Failed to initialize: {e}")
            self.use_supabase = False
    
    def _save(self, name, content):
        """
        Save file to Supabase Storage or fallback storage.
        """
        print(f"[Supabase] _save called: name={name}, use_supabase={self.use_supabase}")
        if not self.use_supabase:
            print(f"[Supabase] Falling back to local storage for: {name}")
            return self.fallback_storage._save(name, content)
        
        # Generate unique filename if needed
        if not name:
            name = f"{uuid.uuid4()}.{content.name.split('.')[-1]}"
        
        # Read file content
        content.seek(0)
        file_content = content.read()
        
        # Upload to Supabase
        name = name.replace('\\', '/')
        content_type = content.content_type if hasattr(content, 'content_type') else 'image/jpeg'
        print(f"[Supabase] Uploading '{name}' to bucket '{self.bucket_name}' ({len(file_content)} bytes, type={content_type})")
        try:
            result = self.supabase.storage.from_(self.bucket_name).upload(
                path=name,
                file=file_content,
                file_options={
                    'content-type': content_type,
                    'upsert': 'true'
                }
            )
            print(f"[Supabase] Upload SUCCESS: {name}")
            return name
        except Exception as e:
            import traceback
            print(f"[Supabase] Upload FAILED: {e}")
            print(f"[Supabase] Traceback: {traceback.format_exc()}")
            return self.fallback_storage._save(name, content)
    
    def url(self, name):
        """
        Get public URL for the file.
        """
        if not self.use_supabase:
            return self.fallback_storage.url(name)
        
        name = name.replace('\\', '/')
        try:
            supabase_url = getattr(settings, 'SUPABASE_URL', '').rstrip('/')
            result = f"{supabase_url}/storage/v1/object/public/{self.bucket_name}/{name}"
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
    
    def deconstruct(self):
        return ('users.storage.SupabaseStorage', [], {})

    def get_available_name(self, name, max_length=None):
        """
        Generate a unique filename if the file already exists.
        """
        if self.exists(name):
            base, ext = os.path.splitext(name)
            name = f"{base}_{uuid.uuid4().hex[:8]}{ext}"
        return name
