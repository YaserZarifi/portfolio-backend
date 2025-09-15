

from rest_framework import serializers
from .models import Tag, Project, Skill, Experience, Education , Certificate, Issuer, Message, Profile

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'long_description', 'image', 'tags', 'live_link', 'repo_link', 'order']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'icon_url', 'order', 'category']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'role', 'company', 'period', 'description', 'order']

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'degree', 'institution', 'period', 'order']

class IssuerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issuer
        fields = ['id', 'name', 'logo','logo_url']


class CertificateSerializer(serializers.ModelSerializer):
    issuer = IssuerSerializer(read_only=True)
    class Meta:
        model = Certificate
        fields = ['id', 'title', 'issuer', 'issue_date', 'credential_id', 'credential_url', 'pdf_file', 'order']



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'name', 'email', 'message', 'created_at']




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'title', 'bio', 'resume_file']



        
