from django.shortcuts import redirect
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, BaseRegisterForm
from .filters import NewsFilter
from NewsPaper.forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'post_list'
    ordering = ['-time']

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['total'] = Post.objects.all().count
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


class PostListFiltered(ListView):
    model = Post
    template_name = 'post/search.html'
    context_object_name = 'post_list_filtered'
    ordering = ['-time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'post/post_create.html'
    permission_required = ('post.add_post',)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = 'post/post_create.html'
    permission_required = ('post.change_post',)

    def get_object(self, **kwargs):
        return Post.objects.get(pk=self.kwargs.get('pk'))
    

class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'post/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('post.delete_post',)
    

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')