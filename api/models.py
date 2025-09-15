from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Model for your portfolio projects
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    long_description = models.TextField(blank=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="projects")
    live_link = models.URLField(blank=True)
    repo_link = models.URLField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

# Model for your skills
class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('FRONTEND', 'Frontend & Design'),
        ('BACKEND', 'Backend & Languages'),
        ('DATA_TOOLS', 'Data Science & Tools'),
    ]

    name = models.CharField(max_length=100)
    icon_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='FRONTEND')




    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Experience(models.Model):
    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.role} at {self.company}"

# Model for your education
class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.degree


class Issuer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='issuer_logos/', blank=True)
    logo_url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.name

class Certificate(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE, related_name='certificates')
    issue_date = models.DateField()
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    pdf_file = models.FileField(upload_to='certificate_pdfs/', blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return self.title




class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} on {self.created_at.strftime('%Y-%m-%d')}"


class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    resume_file = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.name
