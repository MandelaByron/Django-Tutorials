from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blog
from django.db.models import F
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
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



class BlogCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Blog
    
    fields = ['title', 'category', "content", "thumbnail", "status"]
    
    template_name = 'blog-create.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        context['title']= 'Create Blog'
        #categories and tags
        return context    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    ## Check if the user is staff or not  -> True or False
    def test_func(self): 
        return self.request.user.is_staff

    
    # Optional: If the user fails the test, redirect them
    def handle_no_permission(self):
        messages.warning(self.request, "You don't have permission to create blog posts")
        return redirect('blog-list')
    
class BlogUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Blog
    
    fields = ['title', 'category', "content", "thumbnail", "status"]
    
    template_name = 'blog-update.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        context['title']= 'Update Blog'
        #categories and tags
        return context    
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    ## Check is the authenticated user owns the blog object -> True or False
    def test_func(self): 
        blog = self.get_object()
        
        if self.request.user == blog.author:
            return True
        else:
            return False
    
    # Optional: If the user fails the test, redirect them
    def handle_no_permission(self):
        messages.warning(self.request, "You don't have permission to update this post")
        return redirect('blog-list')
    
class BlogDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Blog

    template_name = 'blog-delete.html'
    
    success_url = reverse_lazy('blog-list')
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        context['title']= 'Delete Blog'
        #categories and tags
        return context    
    
    ## Check is the authenticated user owns the blog object -> True or False
    def test_func(self): 
        blog = self.get_object()
        
        if self.request.user == blog.author:
            return True
        else:
            return False
    
    # Optional: If the user fails the test, redirect them
    def handle_no_permission(self):
        messages.warning(self.request, "You don't have permission to delete this post")
        return redirect('blog-list')