from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based access control.
    """
    class UserType(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'SuperAdmin'
        EDITOR = 'EDITOR', 'Editor'

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.EDITOR
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_superadmin(self):
        return self.user_type == self.UserType.SUPERADMIN

    def is_editor(self):
        return self.user_type == self.UserType.EDITOR

    def can_manage_users(self):
        """Only SuperAdmin can manage users"""
        return self.user_type == self.UserType.SUPERADMIN

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Profile(models.Model):
    """
    Profile model for resume/CV website - for Virtual Assistant, Social Media Manager,
    Admin Assistant, Data Annotator, Video and Photo Editor roles.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Basic Information
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    about_image = models.ImageField(upload_to='about_images/', blank=True, null=True)
    title = models.CharField(max_length=200, help_text="Professional title (e.g., Virtual Assistant)")
    bio = models.TextField(help_text="Short professional biography")
    hero_description = models.TextField(blank=True, help_text="Short tagline shown on the hero section")
    full_name = models.CharField(max_length=200, blank=True)
    
    # Contact Information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    website_url = models.URLField(blank=True)
    
    # Social Media Links
    linkedin_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Services Offered
    services_offered = models.JSONField(default=list, blank=True, help_text="List of services offered")
    
    # Skills
    skills = models.JSONField(default=list, blank=True, help_text="List of skills")
    
    # Availability
    is_available = models.BooleanField(default=True, help_text="Available for new projects")
    
    # Section Visibility (for portfolio display)
    show_services = models.BooleanField(default=True, help_text="Show services section in portfolio")
    show_skills = models.BooleanField(default=True, help_text="Show skills section in portfolio")
    show_experience = models.BooleanField(default=True, help_text="Show work experience section in portfolio")
    show_education = models.BooleanField(default=True, help_text="Show education section in portfolio")
    show_projects = models.BooleanField(default=True, help_text="Show portfolio projects section in portfolio")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name or self.user.username} - {self.title}"


class Experience(models.Model):
    """Work experience entries for the profile"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if current")
    is_current = models.BooleanField(default=False)
    description = models.TextField(help_text="Job responsibilities and achievements")
    is_visible = models.BooleanField(default=True, help_text="Show this experience in portfolio")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.job_title} at {self.company}"


class Education(models.Model):
    """Education entries for the profile"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, help_text="Field of study, achievements, etc.")
    is_visible = models.BooleanField(default=True, help_text="Show this education in portfolio")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.degree} from {self.institution}"


class PortfolioProject(models.Model):
    """Portfolio projects for the profile"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    project_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    video_links = models.JSONField(default=list, blank=True, help_text="List of video URLs (YouTube, Vimeo, etc.)")
    technologies = models.JSONField(default=list, blank=True, help_text="List of technologies/tools used")
    is_visible = models.BooleanField(default=True, help_text="Show this project in portfolio")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    """Additional images for portfolio projects"""
    project = models.ForeignKey(PortfolioProject, on_delete=models.CASCADE, related_name='project_images')
    image = models.ImageField(upload_to='portfolio_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Image for {self.project.title}"
