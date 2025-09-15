

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, ProjectViewSet, SkillViewSet, ExperienceViewSet, EducationViewSet, CertificateViewSet, MessageViewSet, ProfileViewSet, FileUploadTestView


router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'certificates', CertificateViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'profile', ProfileViewSet, basename='profile')


urlpatterns = [
    path('', include(router.urls)),
    path('upload-test/', FileUploadTestView.as_view(), name='upload-test'),
]
