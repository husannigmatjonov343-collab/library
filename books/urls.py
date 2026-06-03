from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('pages/', views.pages, name='pages'),
    path('contact/', views.contact, name='contact'),
    path('books/', views.books_view, name='books'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
]