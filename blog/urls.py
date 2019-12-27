from django.conf.urls import url
from .views import PostListView, PostCreateView
from . import views

# empty route
# blog in name incase multiple apps, the name is used for reverse searching
urlpatterns = [
    url('about/', views.about, name='blog-about'),   
    url('post/new/',PostCreateView.as_view(), name='post-create'),
    url(r'^$', PostListView.as_view(), name='blog-home'), 
]
