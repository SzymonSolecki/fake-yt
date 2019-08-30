from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import LoginForm, RegisterForm, AddVideoForm, AddCommentForm
from .models import Video

from django.core.exceptions import ValidationError

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

        form = AddCommentForm()
        context['form'] = form

        comments = video.comments.all()
        context['comments'] = comments

        return render(request, self.template_name, context)


class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect('home')


class LoginView(generic.View):
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
        context = {}
        form = LoginForm(request.POST)
        context['form'] = form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            messages.error(request, 'Provided data is incorrect.')
            return render(request, self.template_name, context)
        return render(request, self.template_name, context)


class RegisterView(generic.View):
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
        context = {}
        form = RegisterForm(request.POST)
        context['form'] = form

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                messages.error(request, 'User exists.')
                return render(request, self.template_name, context)

            return redirect('home')
        return render(request, self.template_name, context)


# class AddVideoView(generic.View):
#     template_name = 'youtube/add_video.html'
#
#     @method_decorator(login_required)
#     def get(self, request):
#         context = {}
#         messages.get_messages(request)
#         form = AddVideoForm()
#         context['form'] = form
#         return render(request, self.template_name, context)
#
#     @method_decorator(login_required)
#     def post(self, request):
#         form = AddVideoForm(request.POST, request.FILES)
#         context = {}
#         context['form'] = form
#
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             description = form.cleaned_data['description']
#             file = form.cleaned_data['file']
#
#             new_video = Video(title=title,
#                               description=description,
#                               user=request.user,
#                               file=file)
#             new_video.save()
#             return redirect('/video/{}'.format(new_video.id))
#         return render(request, self.template_name, context)


class AddVideoView(generic.CreateView):
    template_name = 'youtube/add_video.html'
    model = Video
    fields = ['title', 'description', 'file']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddVideoView, self).form_valid(form)
