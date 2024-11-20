
from django.contrib import admin
from django.urls import path
from .views import hello_world, home_view, about_view, team_view, services_view

urlpatterns = [
    
    path('', home_view,name='home'),
    path('about/',about_view, name="about" ),
    path('team/',team_view, name="team" ),
    path('services/',services_view, name="services" ),
]