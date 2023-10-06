from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectType, ProjectImage, ContactUs
from .forms import ImageUploadForm

# Create your views here.


def home(request):
    return render(request, 'base/home.html')    

# gets all projects and loads them into the context. Project displays the primary image for each project
def projects(request):
    context = {'projects': Project.objects.all()}
    return render(request, 'base/all_projects.html', context)

# gets project detail by primary key and loads all of the images associated 
# with that project and addes them to the context
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    images = ProjectImage.objects.filter(project=project)
    context = {'project': project, 'images': images}
    return render(request, 'base/project_detail.html', context)

def contact(request):
    if request.method == 'POST':
        ContactUs.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            message=request.POST['message']
        )
        return redirect('home')
    else:
        return render(request, 'base/contact.html')

@login_required
def upload_images(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for uploaded_file in request.FILES.getlist('images'):
                ProjectImage.objects.create(project=project, image=uploaded_file)
            return redirect('home')
    else:
        form = ImageUploadForm()

    context = {'form': form, 'project': project}
    return render(request, 'base/upload_images.html', context)