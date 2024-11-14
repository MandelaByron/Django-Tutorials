from django.shortcuts import render
from payments.models import MembershipPlan
from django.contrib.auth.decorators import login_required
# Create your views here.

def services_view(request):
    return render(request,template_name='services.html',context={'title': 'Services'})

def home_view(request):
    plans = MembershipPlan.objects.all()
    return render(request,template_name='index.html',context={'title': 'Home', 'plans': plans})

def about_view(request):
    return render(request,template_name='about-us.html',context={'title': 'About'})

def team_view(request):
    return render(request,template_name='team.html',context={'title': 'Team'})


