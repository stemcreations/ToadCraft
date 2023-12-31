import os
from django.core import serializers
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Project, ProjectType, ProjectImage, ContactUs
from .forms import ImageUploadForm, ProjectForm, ProjectTypeForm, ProjectImageForm, CustomerForm

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
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/contact.html', context)

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

# ------------------ ADMIN DASHOBOARD ------------------ #
@login_required(login_url='login_page')
def admin_panel(request):
        
    projects = Project.objects.all()
    images = ProjectImage.objects.all()
    project_types = ProjectType.objects.all()

    projects_json = serializers.serialize('json', projects)
    images_json = serializers.serialize('json', images)
    project_types_json = serializers.serialize('json', project_types)

    context = {'projects_json': projects_json, 'images_json': images_json, 'project_types_json': project_types_json, 'projects': projects, 'images': images, 'project_types': project_types}
    return render(request, 'base/dashboard.html', context)

# ------------------ ADMIN PROJECTS ------------------ #
@login_required(login_url='login_page')
def admin_panel_projects(request):
    projects = Project.objects.all()
    form = ProjectForm()

    # if the form_type is createProjectForm, then the user is trying to create a new project
    # if the form_type is deleteForm, then the user is trying to delete a project
    if request.method == 'POST':
        if request.POST.get("form_type") == 'createProjectForm':
            form = ProjectForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin_projects')
        elif request.POST.get("form_type") == 'deleteForm':
            project_id = request.POST.get('selected_project')
            project = Project.objects.get(pk=project_id)
            
            # delete project and all associated images from the database and file system
            images = ProjectImage.objects.filter(project=project)
            for image in images:
                image_path = image.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)
                image.delete()
            project.delete()
            return redirect('admin_projects')
        
    context = {'projects': projects, 'form': form}
    return render(request, 'base/admin_projects.html', context)

# ------------------ ADMIN PROJECT DETAILS ------------------ #
@login_required(login_url='login_page')
def admin_project_details(request, pk):
    project = get_object_or_404(Project, pk=pk)
    images = ProjectImage.objects.filter(project=project)
    form = ProjectForm(instance=project)
    image_form = ImageUploadForm()

    # if the form_type is imageForm, then the user is trying to upload images
    if request.method == 'POST':
        if request.POST.get("form_type") == 'imageForm':
            image_form = ImageUploadForm(request.POST, request.FILES)
            if image_form.is_valid():
                for uploaded_file in request.FILES.getlist('images'):
                    ProjectImage.objects.create(project=project, image=uploaded_file)
                return redirect('admin_project_detail', pk=pk)
            
        # if the form_type is projectForm, then the user is trying to edit the project
        elif request.POST.get("form_type") == 'projectForm':
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                selected_image = request.POST.get('selected_image')

                # if the user selected a primary image, then set the primary image to the selected image
                if selected_image:
                    project.primary_image = ProjectImage.objects.get(pk=selected_image)
                    project.name = request.POST['name']
                    project.description = request.POST['description']
                    project.project_type.id = request.POST.get('project_type')
                    project.save()

                # if the user did not select a primary image, then save the other project details
                else:
                    project.name = request.POST['name']
                    project.description = request.POST['description']
                    project.project_type.id = request.POST.get('project_type')
                    project.save()
                return redirect('admin_project_detail', pk=pk)

    context = {'project': project, 'images': images, 'form': form, 'image_form': image_form}
    return render(request, 'base/admin_project_details.html', context)

# ------------------ ADMIN PROJECT TYPES ------------------ #
@login_required(login_url='login_page')
def admin_project_types(request):
    projects = Project.objects.all()
    images = ProjectImage.objects.all()
    project_types = ProjectType.objects.all()
    grouped_projects = {}
    grouped_images = {}
    
    # if the form_type is createProjectTypeForm, then the user is trying to create a new project type
    if request.method == 'POST':
            if request.POST.get("form_type") == 'createProjectTypeForm':
                form = ProjectTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('admin_project_types')
            elif request.POST.get("form_type") == 'deleteForm':
                project_type_id = request.POST.get('selected_project')
                project_type = ProjectType.objects.get(pk=project_type_id)
                project_type.delete()
                return redirect('admin_project_types')
            
    # group projects by project type
    for project in projects:
        # check for none type project type and skip it
        if project.project_type is not None:
            if project.project_type.name in grouped_projects:
                grouped_projects[project.project_type.name].append(project)
            else:
                grouped_projects[project.project_type.name] = [project]
    
    # group images by project type
    for image in images:
        if image.project.project_type is not None:
            if image.project.project_type.name in grouped_images:
                grouped_images[image.project.project_type.name].append(image)
            else:
                grouped_images[image.project.project_type.name] = [image]
    
    form = ProjectTypeForm()
    context = {'form': form, 'projects': projects, 'grouped_projects': grouped_projects, 'grouped_images': grouped_images, 'project_types': project_types}
    return render(request, 'base/admin_project_types.html', context)

# ------------------ ADMIN IMAGES ------------------ #
@login_required(login_url='login_page')
def admin_images(request):
    images = ProjectImage.objects.all()
    projects = Project.objects.all()

    # if the form_type is deleteForm, then the user is trying to delete an image
    if request.method == 'POST':
        if request.POST.get("form_type") == 'deleteForm':
            image_id = request.POST.get('selected_image')
            image = ProjectImage.objects.get(pk=image_id)
            image_path = image.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
            image.delete()
            return redirect('admin_images')

    context = {'images': images, 'projects': projects}
    return render(request, 'base/admin_images.html', context)

# ------------------ ADMIN CUSTOMERS ------------------ #
@login_required(login_url='login_page')
def admin_customers(request):
    customers = ContactUs.objects.all()

    # if the form_type is deleteForm, then the user is trying to delete a customer
    if request.method == 'POST':
        if request.POST.get("form_type") == 'deleteForm':
            customer_id = request.POST.get('selected_customer')
            customer = ContactUs.objects.get(pk=customer_id)
            customer.delete()
            return redirect('admin_customers')

    context = {'customers': customers}
    return render(request, 'base/customers.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

# def send_email(request):
#     s = smtplib.SMTP('smtp.gmail.com', 587)
#     s.starttls()
#     s.login("email", "password")
#     message = "Message_you_need_to_send"
#     s.sendmail("from_email", "to_email", message)
#     s.quit()
#     return redirect('home')