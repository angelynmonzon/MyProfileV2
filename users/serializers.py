from rest_framework import serializers
from .models import User, Profile, Experience, Education, PortfolioProject, ProjectImage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'user_type', 'password', 'password_confirm'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'user_type', 'is_active'
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            'id', 'job_title', 'company', 'location', 'start_date',
            'end_date', 'is_current', 'description', 'is_visible', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id', 'degree', 'institution', 'location', 'start_date',
            'end_date', 'is_current', 'description', 'is_visible', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'image_url', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            if url.startswith('http'):
                return url
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class PortfolioProjectSerializer(serializers.ModelSerializer):
    project_images = ProjectImageSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioProject
        fields = [
            'id', 'title', 'description', 'project_url', 'image', 'image_url',
            'project_images', 'video_links', 'technologies', 'is_visible', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            if url.startswith('http'):
                return url
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            return url
        return None

    def to_internal_value(self, data):
        import json
        if 'technologies' in data and isinstance(data.get('technologies'), str):
            try:
                data = data.copy()
                data['technologies'] = json.loads(data['technologies'])
            except (json.JSONDecodeError, AttributeError):
                pass
        if 'video_links' in data and isinstance(data.get('video_links'), str):
            try:
                data = data.copy()
                data['video_links'] = json.loads(data['video_links'])
            except (json.JSONDecodeError, AttributeError):
                pass
        return super().to_internal_value(data)


class ProfileSerializer(serializers.ModelSerializer):
    experiences = ExperienceSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    projects = PortfolioProjectSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    profile_image_url = serializers.SerializerMethodField()
    about_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'username', 'profile_image', 'profile_image_url', 'about_image', 'about_image_url', 'title', 'bio', 'hero_description', 'full_name',
            'email', 'phone', 'location', 'website_url',
            'linkedin_url', 'facebook_url', 'instagram_url', 'twitter_url', 'github_url',
            'services_offered', 'skills', 'is_available',
            'show_services', 'show_skills', 'show_experience', 'show_education', 'show_projects',
            'experiences', 'education', 'projects',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            url = obj.profile_image.url
            if url.startswith('http'):
                return url
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            return url
        return None

    def get_about_image_url(self, obj):
        if obj.about_image:
            url = obj.about_image.url
            if url.startswith('http'):
                return url
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'profile_image', 'about_image', 'title', 'bio', 'hero_description', 'full_name',
            'email', 'phone', 'location', 'website_url',
            'linkedin_url', 'facebook_url', 'instagram_url', 'twitter_url', 'github_url',
            'services_offered', 'skills', 'is_available',
            'show_services', 'show_skills', 'show_experience', 'show_education', 'show_projects'
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Profile.objects.create(**validated_data)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'profile_image', 'about_image', 'title', 'bio', 'hero_description', 'full_name',
            'email', 'phone', 'location', 'website_url',
            'linkedin_url', 'facebook_url', 'instagram_url', 'twitter_url', 'github_url',
            'services_offered', 'skills', 'is_available',
            'show_services', 'show_skills', 'show_experience', 'show_education', 'show_projects'
        ]
