from django.urls import path
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateview,
    PostDeleteView,
    UserPostListView
)
from . import views
from django.urls import path, include
from .views import *



urlpatterns = [
    path('', PostListView.as_view(), name='mpesaApp-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateview.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='mpesaApp-about'),


    path('api/fetch_payments/',fetch_payments,name='fetch_payments'),
    path('lmp/',lmp,name='lmp'),
]