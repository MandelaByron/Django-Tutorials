from django.contrib import admin
from django.urls import path, include
from .views import services_view, home_view, about_view, team_view
urlpatterns = [
    path('', home_view, name ='home'),
    path('services/', services_view, name ='services'),
    path('about/', about_view, name='about'),
    path('team/', team_view, name='team'),

    
    
]