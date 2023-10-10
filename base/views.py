from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Project, ProjectType, ProjectImage, ContactUs
from .forms import ImageUploadForm

# Create your views here.


def home(request):
    return render(request, 'base/home.html')    

# gets all projects and loads them into the context. Project displays the primary image for each project
def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
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

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_panel')
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_panel')
            else:
                print('login failed')
        except Exception as e:
            print(e)
    return render(request, 'base/login.html')

@login_required(login_url='login_page')
def admin_panel(request):
        
    projects = Project.objects.all()
    images = ProjectImage.objects.all()
    project_types = ProjectType.objects.all()

    context = {'projects': projects, 'images': images, 'project_types': project_types}
    return render(request, 'base/dashboard.html', context)

@login_required(login_url='login_page')
def admin_panel_projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'base/projects_admin.html', context)

@login_required(login_url='login_page')
def admin_project_types(request):
    project_types = ProjectType.objects.all()
    context = {'project_types': project_types}
    return render(request, 'base/project_types_admin.html', context)

@login_required(login_url='login_page')
def admin_images(request):
    images = ProjectImage.objects.all()
    context = {'images': images}
    return render(request, 'base/images_admin.html', context)

@login_required(login_url='login_page')
def admin_customers(request):
    customers = ContactUs.objects.all()
    context = {'customers': customers}
    return render(request, 'base/customers.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')