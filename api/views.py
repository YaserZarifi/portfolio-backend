from rest_framework import viewsets,status
from .models import Tag, Project, Skill, Experience, Education, Certificate, Message
from .serializers import TagSerializer, ProjectSerializer, SkillSerializer, ExperienceSerializer, EducationSerializer, CertificateSerializer, MessageSerializer
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.response import Response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all().order_by('order')
    serializer_class = ProjectSerializer

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
