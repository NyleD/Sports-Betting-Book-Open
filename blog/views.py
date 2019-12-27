from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def about(request):
    return render(request, 'blog/about.html', {'title' : 'About'})

@login_required
def home(request):
    context = {
        'posts' : Post.objects.all(),
    }
    return render(request, 'blog/home.html',context)  # landed on the blog home page


# alternate to function view called home
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts' # default one is <object name>_list
    ordering = ['-date_posted'] # the minus sign makes it newest to oldest


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


