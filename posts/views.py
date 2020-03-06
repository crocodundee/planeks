from posts.models import Post, Comment
from posts.forms import PostForm, CommentForm
from users.tasks import send_comment_info_mail

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ModelFormMixin
from django.shortcuts import redirect
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)


class PostView(ModelFormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        post = Post.objects.get(slug=self.kwargs.get('slug'))
        context['comments'] = Comment.objects.filter(post=post).order_by('-created_at')
        context['title'] = post.title
        return context

    def form_valid(self, form):
        new_comment = Comment.objects.create(
            post=self.object,
            author=self.request.user,
            content=form.cleaned_data['content']
        )
        new_comment.save()
        send_comment_info_mail(new_comment.id)
        return redirect('post-view', self.object.slug)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return redirect('login')


class PostList(ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['posts'] = Post.objects.approved_posts()
        except Post.DoesNotExist:
            context['posts'] = None
        context['title'] = 'Главная'
        return context


class PostCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = '/post/{slug}'
    success_message = f'Публикация успешно создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = '/post/{slug}'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name_suffix = '_delete'
    success_url = ''

