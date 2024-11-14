from django.urls import path, include
from .views import blog_list, blog_detail, UserBlogListView,BlogDetailView, BlogListView , BlogCategoryListView, BlogCreateView, BlogUpdateView, BlogDeleteView
urlpatterns = [
    
    path('', BlogListView.as_view(), name ='blog-list'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('user/<uuid:public_id>/', UserBlogListView.as_view(), name='user_blogs'),
    path('update/<slug:slug>/', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<slug:slug>/', BlogDeleteView.as_view(), name='blog_delete'),
    path('category/<str:category>/', BlogCategoryListView.as_view(), name='blog_by_category'),
    path('content/new/', BlogCreateView.as_view(), name='blog_create'),


    
]