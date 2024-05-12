from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.forms import PostForm
from .models import *
from django.urls import reverse_lazy

def index(request):
    return render(request,'blog/index.html')
class Post_listView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'

class DetailPost(DetailView):
    model = Post
    template_name = 'blog/detailPost.html'
    context_object_name = 'post'

@method_decorator(login_required, name='dispatch')
class CreerPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/addPost.html'
    form_class = PostForm 
    success_url = reverse_lazy('post-list') 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreerPost, self).form_valid(form)


class ModifierPost(UpdateView):
    model = Post
    template_name = 'blog/editPost.html'
    form_class = PostForm 
    success_url = reverse_lazy('post-list') 
class SupprimerPost(DeleteView):
    model = Post
    template_name = 'blog/deletePost.html'
    success_url = reverse_lazy('post-list') 



