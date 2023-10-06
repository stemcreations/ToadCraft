from django.contrib import admin
from .models import Project, ProjectType, ProjectImage, ContactUs


admin.site.register(Project)
admin.site.register(ProjectType)
admin.site.register(ProjectImage)
admin.site.register(ContactUs)