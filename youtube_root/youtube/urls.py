from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('add_video/', views.AddVideoView.as_view(), name='add_video'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('video/<pk>/', views.VideoView.as_view(), name='video'),
    path('video/<pk>/comment', views.AddCommentView.as_view()),
    path('video/<pk>/like', views.LikeVideoView.as_view()),
    path('video/<pk>/dislike', views.DislikeVideoView.as_view()),
]
