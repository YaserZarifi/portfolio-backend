from rest_framework import viewsets,status
from .models import Tag, Project, Skill, Experience, Education, Certificate, Message, Profile,Category
from .serializers import TagSerializer, ProjectSerializer, SkillSerializer, ExperienceSerializer,ProfileSerializer, EducationSerializer, CertificateSerializer, MessageSerializer,CategorySerializer
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

class HealthCheckView(APIView):
    """
    A simple view to check if the server is running.
    """
    def get(self, request, format=None):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all().order_by('order')
    serializer_class = ProjectSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all().order_by('order')
    serializer_class = SkillSerializer


class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.all().order_by('order')
    serializer_class = ExperienceSerializer

class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Education.objects.all().order_by('order')
    serializer_class = EducationSerializer

class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certificate.objects.all().order_by('order', '-issue_date')
    serializer_class = CertificateSerializer




class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)


        try:
            subject = f"New Portfolio Message from {serializer.data['name']}"
            message_body = f"""
        You received a new message from your portfolio contact form.

        Name: {serializer.data['name']}
        Email: {serializer.data['email']}

        Message:
        {serializer.data['message']}
            """


            email = EmailMessage(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                reply_to=[serializer.data['email']]
            )
            email.send(fail_silently=False)

        except Exception as e:
            print(f"Email failed to send: {e}")
            pass

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # This custom action ensures we only ever get one profile
    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status


class FileUploadTestView(APIView):
    """
    A simple view to test uploading a resume file.
    It finds the *first* profile and updates its resume_file.
    Send a POST request with 'resume_file' as a form-data key.
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        # Get the file from the request
        file_obj = request.data.get('resume_file')
        if not file_obj:
            return Response({'error': 'File not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the first profile object to update
        profile = Profile.objects.first()
        if not profile:
            return Response({'error': 'No profile found in the database'}, status=status.HTTP_404_NOT_FOUND)

        # Assign the file and save
        try:
            profile.resume_file = file_obj
            profile.save()

            # Return the URL from the storage backend
            file_url = profile.resume_file.url
            return Response({
                'message': 'File uploaded successfully!',
                'file_url': file_url
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
