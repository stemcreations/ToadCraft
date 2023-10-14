
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
    tailwind_css = """w-full border-2 border-ch-gray-light 
        bg-ch-gray-dark rounded-lg 
        focus:outline-ch-green-light focus:outline-0 
        focus:outline-offset-0 focus:border-2 
        focus:border-woys-purple focus:shadow-none 
        focus:ring-0 focus:shadow-0"""
    
    name = forms.CharField(widget=forms.TextInput(attrs={'class': tailwind_css}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': tailwind_css}))
    project_type = forms.ModelChoiceField(queryset=ProjectType.objects.all(), widget=forms.Select(attrs={'class': tailwind_css}))

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

# contact us form
class CustomerForm(forms.ModelForm):
    tailwind_class = """w-full border-2 border-ch-gray-light 
        bg-ch-gray-dark rounded-lg 
        focus:outline-ch-green-light focus:outline-0 
        focus:outline-offset-0 focus:border-2 
        focus:border-woys-purple focus:shadow-none 
        focus:ring-0 focus:shadow-0"
        """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': tailwind_class}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': tailwind_class}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': tailwind_class}))
    project_type = forms.ModelChoiceField(queryset=ProjectType.objects.all(), widget=forms.Select(attrs={'class': tailwind_class}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': tailwind_class}))

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone', 'project_type', 'message']


