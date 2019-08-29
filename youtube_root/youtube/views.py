from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import LoginForm, RegisterForm, AddVideoForm
from .models import Video

import string
import random

# Create your views here.


class HomeView(View):
    template_name = 'youtube/home.html'

    def get(self, request):
        context = {}
        recent_videos = Video.objects.order_by('-date_added')[:8]
        context['recent_videos'] = recent_videos
        return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class LoginView(View):
    template_name = 'youtube/login.html'

    def get(self, request):
        context = {}
        messages.get_messages(request)

        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            messages.error(request, 'Provided data is incorrect.')
            return redirect('login')
        messages.error(request, 'Something went wrong.')
        return redirect('login')


class RegisterView(View):
    template_name = 'youtube/register.html'

    def get(self, request):
        context = {}
        messages.get_messages(request)

        if request.user.is_authenticated:
            return redirect('home')

        form = RegisterForm()
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                messages.error(request, 'User exists.')
                return redirect('register')

            return redirect('home')
        messages.error(request, 'One of fields incorrect.')
        return redirect('register')


class AddVideoView(View):
    template_name = 'youtube/add_video.html'

    @method_decorator(login_required)
    def get(self, request):
        context = {}
        messages.get_messages(request)
        form = AddVideoForm()
        context['form'] = form
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = AddVideoForm(request.POST, request.FILES)
        print(form)
        print(request.POST)
        print(request.FILES)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']

            new_video = Video(title=title,
                              description=description,
                              user=request.user,
                              file=file)
            new_video.save()
            return redirect('/video/{}'.format(new_video.id))
        messages.error(request, 'One of the field is incorrect')
        return redirect('add_video')
