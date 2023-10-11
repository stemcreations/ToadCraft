
from django import forms 
from .models import Project, ProjectImage, ProjectType, ContactUs

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImageUploadForm(forms.Form):
    images = MultipleFileField()


# edit project form
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'primary_image', 'project_type']

# edit project type form
class ProjectTypeForm(forms.ModelForm):
    class Meta:
        model = ProjectType
        fields = "__all__"

# edit project image form
class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = "__all__"



