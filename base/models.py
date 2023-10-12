from django.db import models

# Create your models here.
 
 # project model where many images have a many to many relationship with the project type.
 # project types include stickers, vinyl wraps, banners and custom graphics. the admin can add more project types as needed.

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project_type = models.ForeignKey('ProjectType', null=True, blank=True, on_delete=models.SET_NULL)
    primary_image = models.ForeignKey('ProjectImage', on_delete=models.CASCADE, related_name='primary_image', null=True, blank=True)

    def __str__(self):
        return self.name
    
class ProjectType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"Image for {self.project.name}"


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name