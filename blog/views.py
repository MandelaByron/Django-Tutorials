from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Blog
from django.db.models import F

class BlogListView(ListView):
    #model = Blog #Blog.objects.all() -> queryset
    queryset = Blog.published.all()
    
    #Blog.published.all()
    
    template_name = "blog-list.html"
    
    context_object_name = "blog_posts"

    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        context['title']= "Blog Posts"
        #categories and tags
        return context
    
    
class BlogDetailView(DetailView):
    model = Blog 

    
    template_name = "blog-detail.html"
    
    context_object_name = "blog_post"

    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        context['title']= self.object.title
        #categories and tags
        return context 
    
    def get_object(self, queryset = None):
        blog = super().get_object(queryset)
        
        Blog.objects.filter(pk=blog.pk).update(viewCount = F(name="viewCount") + 1)
        
        return blog
        #F reference a model field in a query and perform operations directly on it at the database level
        # Without F expression
        
        # blog = Blog.objects.get(pk=blog.pk) 10
        # blog.viewCount += 1 # Both increase it by 1.
        # blog.save() # The last save overwrites the other
        
        ##http://localhost:8000/blog/plant-based-protein-the-best-the-worst-and-everything-in-between/ 


    