from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'aboutme/index.html')

def contributors(request):
    return render(request, 'aboutme/contributors.html')

def about(request):
    return render(request, 'aboutme/about.html')