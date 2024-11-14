from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView , UpdateView, DeleteView
from .models import Blog
from django.db.models import Count, F , Sum
from .forms import BlogCreateForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from users.models import CustomUser
# Create your views here.
def blog_list(request):
    
    return render(request, 'blog-list.html')

def blog_detail(request):
    
    return render(request, 'blog-detail.html')


class UserBlogListView(ListView):
    model = Blog
    
    template_name = 'blog-list.html'
    
    paginate_by = 3
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, public_id=self.kwargs.get('public_id'))
        context['title'] = f"{user.first_name}'s Blogs"
        #context['title'] = 'User Blogs'
        
        context['categories'] = Blog.objects.values('category').annotate(category_count=Count('category')).order_by()
        
        context['popular_tags'] = Blog.objects.values('tags__name').annotate(total_views=Sum('view_count')).order_by('-total_views')[:10]
        
        return context  
    
    def get_queryset(self) -> QuerySet[Any]:
        user = get_object_or_404(CustomUser, public_id = self.kwargs.get('public_id'))
        return Blog.objects.filter(author=user)
    
class BlogListView(ListView):
    model = Blog
    
    template_name = 'blog-list.html'
    
    paginate_by = 3
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
             
        context['title'] = 'Blog'
        
        context['categories'] = Blog.objects.values('category').annotate(category_count=Count('category')).order_by()
        
        context['popular_tags'] = Blog.objects.values('tags__name').annotate(total_views=Sum('view_count')).order_by('-total_views')[:10]
        
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return Blog.published.all()
class BlogCategoryListView(ListView):
    model = Blog
    template_name = 'blog-list.html'
    context_object_name = 'blog_posts'

    paginate_by = 3
    def get_queryset(self):
        category = self.kwargs.get('category')

        return Blog.objects.filter(category=category)  # Filter posts by the selected category

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
             
        context['title'] = 'Blog'
        
        context['categories'] = Blog.objects.values('category').annotate(category_count=Count('category')).order_by()
        
        context['popular_tags'] = Blog.objects.values('tags__name').annotate(total_views=Sum('view_count')).order_by('-total_views')[:10]
        
        return context
    
class BlogDetailView(DetailView):
    
    model = Blog
    
    template_name = 'blog-detail.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context['title'] = self.object.title
        
        return context
    
    def get_object(self, queryset=None):
        blog = super().get_object(queryset)
        Blog.objects.filter(pk=blog.pk).update(view_count=F('view_count') + 1)
        return blog
    

class BlogCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    
    model = Blog
    
    form_class = BlogCreateForm
    
    template_name = 'blog-create.html'
    
    #success_url = '/'
    def get_success_url(self):
        # Redirect to the detail page of the created blog post
        return reverse('blog_detail', kwargs={'slug': self.object.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Blog Create'  
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        
        #form.instance.image = self.request.FILES.get('image') 
        
        return super().form_valid(form)
  # This method checks if the current user is an admin
    def test_func(self):
        return self.request.user.is_staff  # Only staff/admin users can create blogs

    # Optional: If the user fails the test, redirect them
    def handle_no_permission(self):
        
        messages.warning(self.request, "You do not have permission to create a blog post.")
        return redirect('profile')  # Redi



class BlogUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Blog
    
    fields = ['title', 'content','thumbnail']
    
    template_name = 'blog-update.html'
    
    #success_url = '/'
    def get_success_url(self):
        # Redirect to the detail page of the created blog post
        return reverse('blog_detail', kwargs={'slug': self.object.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Blog Update'  
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        
        return super().form_valid(form)
  # This method checks if the current user is an admin
    def test_func(self):
        blog = self.get_object()       
        
        if (self.request.user == blog.author) or self.request.user.is_staff:
            return True   
        else:
            
            return False # Only staff/admin users can create blogs

    # Optional: If the user fails the test, redirect them
    def handle_no_permission(self):
        
        messages.warning(self.request, "You do not have permission to edit this post.")
        return redirect('blog-list') 
    
class BlogDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Blog

    template_name = 'blog-delete.html'
    
    success_url = '/'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Blog Delete'  
        return context

  # This method checks if the current user is an admin
    def test_func(self):
        blog = self.get_object()       
        
        if (self.request.user == blog.author) or self.request.user.is_staff:
            return True   
        else:
            
            return False # Only staff/admin users can create blogs

    # Optional: If the user fails the test, redirect them
    def handle_no_permission(self):
        
        messages.warning(self.request, "You do not have permission to delete this post.")
        return redirect('blog-list') 