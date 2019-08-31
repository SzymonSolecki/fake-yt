from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import IntegrityError

from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import LoginForm, RegisterModelForm, AddVideoModelForm, AddCommentModelForm
from .models import Video

from django.core.exceptions import ValidationError

from django.urls import reverse, reverse_lazy

from django.contrib.auth.forms import AuthenticationForm
# Create your views here.


class HomeView(generic.ListView):
    template_name = 'youtube/home.html'

    def get_queryset(self):
        recent_videos = Video.objects.order_by('-date_added')[:8]
        return recent_videos


class VideoView(generic.View):
    template_name = 'youtube/video.html'

    def get(self, request, pk):
        context = {}
        messages.get_messages(request)
        video = get_object_or_404(Video, pk=pk)
        context['video'] = video

        form = AddCommentModelForm()
        context['form'] = form

        comments = video.comments.all()
        context['comments'] = comments

        return render(request, self.template_name, context)


class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect('home')


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'youtube/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super(LoginView, self).form_valid(form)


class RegisterView(UserPassesTestMixin, generic.CreateView):
    template_name = 'youtube/register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('home')

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('home')


class AddVideoView(LoginRequiredMixin, generic.CreateView):
    template_name = 'youtube/add_video.html'
    form_class = AddVideoModelForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddVideoView, self).form_valid(form)
