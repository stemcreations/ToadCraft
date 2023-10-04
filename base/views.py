from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'base/home.html')    

def projects(request):
    return render(request, 'base/all_projects.html')

def project_detail(request, pk):
    context = {}
    return render(request, 'base/project_detail.html', context)

def contact(request):
    return render(request, 'base/contact.html')