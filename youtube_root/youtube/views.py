from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

from .forms import LoginForm, RegisterModelForm, AddVideoModelForm, AddCommentModelForm
from .models import Video, Comment, Like

from django.urls import reverse, reverse_lazy


class HomeView(generic.ListView):
    template_name = 'youtube/home.html'

    def get_queryset(self):
        recent_videos = Video.objects.order_by('-date_added')[:8]
        return recent_videos


class AddCommentView(LoginRequiredMixin, generic.RedirectView):
    pattern_name = 'video'

    def post(self, *args, **kwargs):
        form = AddCommentModelForm(self.request.POST)
        comment = Comment(owner=self.request.user,
                          video=Video.objects.get(pk=kwargs.get('pk')))
        if form.is_valid():
            comment.text = form.cleaned_data['text']
            comment.save()
            messages.success(self.request, 'Comment added successfully.')
        else:
            messages.error(self.request, "Comment not added.")
        return super().post(*args, **kwargs)


class VideoView(generic.DetailView):
    template_name = 'youtube/video.html'
    model = Video

    def get(self, *args, **kwargs):
        video = get_object_or_404(Video, pk=self.kwargs.get('pk'))
        video.views += 1
        video.save()
        return super(VideoView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        video = get_object_or_404(Video, pk=self.kwargs.get('pk'))
        kwargs['video'] = video
        kwargs['comments'] = video.comments.order_by('-date_added')
        kwargs['likes_count'] = video.likes.filter(value=1).count()
        kwargs['dislikes_count'] = video.likes.filter(value=0).count()
        if self.request.user.is_authenticated:
            try:
                like = Like.objects.get(video=video, user=self.request.user)
            except Like.DoesNotExist:
                kwargs['like'] = -1
            else:
                kwargs['like'] = like.value

        kwargs['form'] = AddCommentModelForm
        return super(VideoView, self).get_context_data(**kwargs)


class LikeVideoView(LoginRequiredMixin, generic.RedirectView):
    pattern_name = 'video'

    def get_redirect_url(self, *args, **kwargs):
        video = Video.objects.get(pk=kwargs['pk'])
        like, created = Like.objects.get_or_create(
            user=self.request.user, video=video)
        if not created:
            if like.value == 0:
                like.value = 1
                like.save()
            else:
                like.delete()
        else:
            like.value = 1
            like.save()
        return super().get_redirect_url(*args, **kwargs)


class DislikeVideoView(LoginRequiredMixin, generic.RedirectView):
    pattern_name = 'video'

    def get_redirect_url(self, *args, **kwargs):
        video = Video.objects.get(pk=kwargs['pk'])
        like, created = Like.objects.get_or_create(
            user=self.request.user, video=video)
        if not created:
            if like.value == 1:
                like.value = 0
                like.save()
            else:
                like.delete()
        else:
            like.value = 0
            like.save()
        return super().get_redirect_url(*args, **kwargs)


class LogoutView(generic.RedirectView):
    pattern_name = 'home'
    success_message = 'Logged in successfully.'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        messages.success(
            self.request, "You have been successfully logged out.")
        return super().get_redirect_url(*args, **kwargs)


class LoginView(UserPassesTestMixin, SuccessMessageMixin, generic.FormView):
    form_class = LoginForm
    template_name = 'youtube/login.html'
    success_url = reverse_lazy('home')
    success_message = 'Logged in successfully.'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super(LoginView, self).form_valid(form)

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(
            self.request, 'You are already logged in. Dont mess with URL.')
        return redirect('home')


class RegisterView(UserPassesTestMixin, generic.CreateView):
    template_name = 'youtube/register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('home')
    success_message = 'User created successfully.'

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(
            self.request, 'You are already logged in. Dont mess with URL.')
        return redirect('home')


class AddVideoView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'youtube/add_video.html'
    form_class = AddVideoModelForm
    success_url = reverse_lazy('home')
    success_message = 'Video added successfully.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddVideoView, self).form_valid(form)
