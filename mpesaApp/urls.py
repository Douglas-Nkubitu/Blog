from django.urls import path
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateview,
    PostDeleteView,
    UserPostListView,
    Mpesa_PaymentsListView
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
    path('payment/', Mpesa_PaymentsListView.as_view(), name='mpesaApp-payment'),


    path('api/fetch_payments/',fetch_payments,name='fetch_payments'),
    path('lipa_na_mpesa',lipa_na_mpesa,name='lipa_na_mpesa'),
]