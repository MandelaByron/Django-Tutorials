from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    
    path('', BlogListView.as_view(), name='blog-list'),
    path('content/new/', BlogCreateView.as_view(), name='blog-create'),
    path('content/update/<slug:slug>/', BlogUpdateView.as_view(), name='blog-update'),
    path('content/delete/<slug:slug>/', BlogDeleteView.as_view(), name='blog-delete'),
    path('<slug:slug>', BlogDetailView.as_view(), name='blog-detail'),
    

]