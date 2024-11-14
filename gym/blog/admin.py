from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Blog

#admin.site.register(Blog)

@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'status','category','view_count']