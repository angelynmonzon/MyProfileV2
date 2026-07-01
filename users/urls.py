from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, LoginView, ProfileViewSet, ExperienceViewSet,
    EducationViewSet, PortfolioProjectViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'education', EducationViewSet, basename='education')
router.register(r'projects', PortfolioProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', csrf_exempt(LoginView.as_view()), name='login'),
]
