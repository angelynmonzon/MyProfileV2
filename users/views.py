from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User, Profile, Experience, Education, PortfolioProject
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    ProfileSerializer, ProfileCreateSerializer, ProfileUpdateSerializer,
    ExperienceSerializer, EducationSerializer, PortfolioProjectSerializer
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

    def get_serializer_class(self):
        if self.action == 'create':
            return ProfileCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProfileUpdateSerializer
        return ProfileSerializer

    def get_permissions(self):
        if self.action == 'public':
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

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get the current user's profile"""
        try:
            profile = request.user.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {'detail': 'Profile not found. Create a profile first.'},
                status=status.HTTP_404_NOT_FOUND
            )

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
        if self.request.user.is_superadmin():
            return Experience.objects.all()
        return Experience.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class EducationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Education model.
    - Users can manage their own education
    - SuperAdmin can manage all education
    """
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superadmin():
            return Education.objects.all()
        return Education.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class PortfolioProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PortfolioProject model.
    - Users can manage their own projects
    - SuperAdmin can manage all projects
    """
    serializer_class = PortfolioProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superadmin():
            return PortfolioProject.objects.all()
        return PortfolioProject.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)
