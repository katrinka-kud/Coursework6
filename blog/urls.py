from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('detail/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='blog_detail'),
    path('blog/create', BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/update', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<int:pk>/delete', BlogDeleteView.as_view(), name='blog_delete'),
]
