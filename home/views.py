from django.shortcuts import render
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello World!")

def home_view(request):
    return render(request, template_name="index.html", context={"title": "Home"})

def about_view(request):
    return render(request, template_name='about-us.html', context={"title": "About Us"})

def services_view(request):
    return render(request, template_name='services.html', context={"title": "Services"})

def team_view(request):
    return render(request, template_name='team.html', context={"title": "Team"})