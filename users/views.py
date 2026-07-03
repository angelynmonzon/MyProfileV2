from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User, Profile, Experience, Education, PortfolioProject, ProjectImage, Testimonial, Certificate
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    ProfileSerializer, ProfileCreateSerializer, ProfileUpdateSerializer,
    ExperienceSerializer, EducationSerializer, PortfolioProjectSerializer, ProjectImageSerializer, TestimonialSerializer, CertificateSerializer
)
from .permissions import IsSuperAdmin, IsSuperAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model with role-based access control.
    - SuperAdmin: Full CRUD access to all users
    - Editor: Read-only access to all users
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Custom permission handling:
        - Only SuperAdmin can create/update/delete users
        - All authenticated users can list/retrieve users
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsSuperAdmin]
        else:
            permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user information"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def editors(self, request):
        """Get all Editor users"""
        if not request.user.is_superadmin():
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        editors = User.objects.filter(user_type=User.UserType.EDITOR)
        serializer = UserSerializer(editors, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def superadmins(self, request):
        """Get all SuperAdmin users"""
        if not request.user.is_superadmin():
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        superadmins = User.objects.filter(user_type=User.UserType.SUPERADMIN)
        serializer = UserSerializer(superadmins, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    Login view for obtaining authentication token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            return Response(
                {'error': f'Authentication error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Profile model.
    - Users can view their own profile and public profiles
    - Users can create and update their own profile
    - SuperAdmin can manage all profiles
    """
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return ProfileCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProfileUpdateSerializer
        return ProfileSerializer

    def get_permissions(self):
        if self.action in ['public', 'public_profile']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Filter queryset based on user permissions:
        - SuperAdmin can see all profiles
        - Regular users can only see their own profile
        """
        if self.action == 'public':
            return Profile.objects.filter(is_available=True)
        if self.request.user.is_authenticated and self.request.user.is_superadmin():
            return Profile.objects.all()
        if self.request.user.is_authenticated:
            return Profile.objects.filter(user=self.request.user)
        return Profile.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        print(f"[DEBUG] PATCH FILES: {request.FILES}")
        print(f"[DEBUG] PATCH DATA keys: {list(request.data.keys())}")
        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get the current user's profile (auto-creates if missing)"""
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def public_profile(self, request):
        """Get the public profile for the portfolio website"""
        public_profile = Profile.objects.filter(is_available=True).first()
        if not public_profile:
            return Response({'detail': 'No public profile found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(public_profile)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def public(self, request):
        """
        Get all public profiles (for public website)
        Only returns profiles where is_available is True
        """
        public_profiles = Profile.objects.filter(is_available=True)
        serializer = ProfileSerializer(public_profiles, many=True)
        return Response(serializer.data)


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Experience model.
    - Users can manage their own experiences
    - SuperAdmin can manage all experiences
    """
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'public':
            return Experience.objects.filter(profile__is_available=True)
        if self.request.user.is_superadmin():
            return Experience.objects.all()
        return Experience.objects.filter(profile__user=self.request.user)

    def get_permissions(self):
        if self.action == 'public':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)

    @action(detail=False, methods=['get'])
    def public(self, request):
        """Get all public experiences for the portfolio website"""
        public_experiences = Experience.objects.filter(profile__is_available=True)
        serializer = ExperienceSerializer(public_experiences, many=True)
        return Response(serializer.data)


class EducationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Education model.
    - Users can manage their own education
    - SuperAdmin can manage all education
    """
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'public':
            return Education.objects.filter(profile__is_available=True)
        if self.request.user.is_superadmin():
            return Education.objects.all()
        return Education.objects.filter(profile__user=self.request.user)

    def get_permissions(self):
        if self.action == 'public':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)

    @action(detail=False, methods=['get'])
    def public(self, request):
        """Get all public education for the portfolio website"""
        public_education = Education.objects.filter(profile__is_available=True)
        serializer = EducationSerializer(public_education, many=True)
        return Response(serializer.data)


class PortfolioProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PortfolioProject model.
    - Users can manage their own projects
    - SuperAdmin can manage all projects
    """
    serializer_class = PortfolioProjectSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        if self.action == 'public':
            return PortfolioProject.objects.filter(profile__is_available=True)
        if self.request.user.is_superadmin():
            return PortfolioProject.objects.all()
        return PortfolioProject.objects.filter(profile__user=self.request.user)

    def get_permissions(self):
        if self.action == 'public':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)

    @action(detail=False, methods=['get'])
    def public(self, request):
        """Get all public projects for the portfolio website"""
        public_projects = PortfolioProject.objects.filter(profile__is_available=True)
        serializer = PortfolioProjectSerializer(public_projects, many=True)
        return Response(serializer.data)


class ProjectImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ProjectImage model.
    - Users can manage images for their own projects
    - SuperAdmin can manage all project images
    """
    serializer_class = ProjectImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superadmin():
            return ProjectImage.objects.all()
        return ProjectImage.objects.filter(project__profile__user=self.request.user)

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        if project_id:
            try:
                project = PortfolioProject.objects.get(id=project_id)
                serializer.save(project=project)
            except PortfolioProject.DoesNotExist:
                raise serializers.ValidationError("Invalid project ID")
        else:
            raise serializers.ValidationError("Project ID is required")


class TestimonialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Testimonial model.
    - Users can manage their own testimonials
    - SuperAdmin can manage all testimonials
    """
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        if self.request.user.is_superadmin():
            return Testimonial.objects.all()
        return Testimonial.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class CertificateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Certificate model.
    - Users can manage their own certificates
    - SuperAdmin can manage all certificates
    """
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        if self.request.user.is_superadmin():
            return Certificate.objects.all()
        return Certificate.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)
