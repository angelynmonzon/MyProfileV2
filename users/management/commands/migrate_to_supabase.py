import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import File
from supabase import create_client
from users.models import Profile, PortfolioProject, ProjectImage


class Command(BaseCommand):
    help = 'Migrate local media files to Supabase Storage'

    def add_arguments(self, parser):
        parser.add_argument(
            '--bucket',
            type=str,
            default=getattr(settings, 'SUPABASE_STORAGE_BUCKET', 'images'),
            help='Supabase storage bucket name'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually uploading'
        )

    def handle(self, *args, **options):
        bucket_name = options['bucket']
        dry_run = options['dry_run']
        
        supabase_url = getattr(settings, 'SUPABASE_URL')
        supabase_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY')
        
        if not supabase_url or not supabase_key:
            self.stdout.write(self.style.ERROR('SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in settings'))
            return
        
        supabase = create_client(supabase_url, supabase_key)
        media_root = getattr(settings, 'MEDIA_ROOT')
        
        self.stdout.write(f'Migrating media files from {media_root} to Supabase bucket: {bucket_name}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No files will be uploaded'))
        
        # Migrate profile images
        self.migrate_profile_images(supabase, bucket_name, media_root, dry_run)
        
        # Migrate portfolio images
        self.migrate_portfolio_images(supabase, bucket_name, media_root, dry_run)
        
        self.stdout.write(self.style.SUCCESS('Migration complete'))

    def migrate_profile_images(self, supabase, bucket_name, media_root, dry_run):
        self.stdout.write('\n--- Migrating Profile Images ---')
        
        profiles = Profile.objects.exclude(profile_image='')
        for profile in profiles:
            if not profile.profile_image:
                continue
                
            local_path = os.path.join(media_root, str(profile.profile_image))
            
            if not os.path.exists(local_path):
                self.stdout.write(self.style.WARNING(f'File not found: {local_path}'))
                continue
            
            supabase_path = str(profile.profile_image)
            
            if dry_run:
                self.stdout.write(f'Would upload: {local_path} -> {supabase_path}')
                continue
            
            try:
                with open(local_path, 'rb') as f:
                    file_content = f.read()
                
                supabase.storage.from_(bucket_name).upload(
                    path=supabase_path,
                    file=file_content,
                    file_options={'content-type': 'image/jpeg', 'upsert': 'true'}
                )
                
                self.stdout.write(self.style.SUCCESS(f'Uploaded: {supabase_path}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to upload {supabase_path}: {str(e)}'))
        
        # Migrate about images
        profiles = Profile.objects.exclude(about_image='')
        for profile in profiles:
            if not profile.about_image:
                continue
                
            local_path = os.path.join(media_root, str(profile.about_image))
            
            if not os.path.exists(local_path):
                self.stdout.write(self.style.WARNING(f'File not found: {local_path}'))
                continue
            
            supabase_path = str(profile.about_image)
            
            if dry_run:
                self.stdout.write(f'Would upload: {local_path} -> {supabase_path}')
                continue
            
            try:
                with open(local_path, 'rb') as f:
                    file_content = f.read()
                
                supabase.storage.from_(bucket_name).upload(
                    path=supabase_path,
                    file=file_content,
                    file_options={'content-type': 'image/jpeg', 'upsert': 'true'}
                )
                
                self.stdout.write(self.style.SUCCESS(f'Uploaded: {supabase_path}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to upload {supabase_path}: {str(e)}'))

    def migrate_portfolio_images(self, supabase, bucket_name, media_root, dry_run):
        self.stdout.write('\n--- Migrating Portfolio Images ---')
        
        # Migrate main project images
        projects = PortfolioProject.objects.exclude(image='')
        for project in projects:
            if not project.image:
                continue
                
            local_path = os.path.join(media_root, str(project.image))
            
            if not os.path.exists(local_path):
                self.stdout.write(self.style.WARNING(f'File not found: {local_path}'))
                continue
            
            supabase_path = str(project.image)
            
            if dry_run:
                self.stdout.write(f'Would upload: {local_path} -> {supabase_path}')
                continue
            
            try:
                with open(local_path, 'rb') as f:
                    file_content = f.read()
                
                supabase.storage.from_(bucket_name).upload(
                    path=supabase_path,
                    file=file_content,
                    file_options={'content-type': 'image/jpeg', 'upsert': 'true'}
                )
                
                self.stdout.write(self.style.SUCCESS(f'Uploaded: {supabase_path}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to upload {supabase_path}: {str(e)}'))
        
        # Migrate additional project images
        project_images = ProjectImage.objects.all()
        for img in project_images:
            if not img.image:
                continue
                
            local_path = os.path.join(media_root, str(img.image))
            
            if not os.path.exists(local_path):
                self.stdout.write(self.style.WARNING(f'File not found: {local_path}'))
                continue
            
            supabase_path = str(img.image)
            
            if dry_run:
                self.stdout.write(f'Would upload: {local_path} -> {supabase_path}')
                continue
            
            try:
                with open(local_path, 'rb') as f:
                    file_content = f.read()
                
                supabase.storage.from_(bucket_name).upload(
                    path=supabase_path,
                    file=file_content,
                    file_options={'content-type': 'image/jpeg', 'upsert': 'true'}
                )
                
                self.stdout.write(self.style.SUCCESS(f'Uploaded: {supabase_path}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to upload {supabase_path}: {str(e)}'))
