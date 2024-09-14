from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import Createview

urlpatterns = [
    path('', views.home, name='main-home'),
    path('adddata/', Createview.as_view(), name='main-adddata'),
    path('register/', views.register, name='main-register'),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='main-login'),
    path('logout/', views.logout_view, name='main-logout'),
    path('profile/', views.profile, name='main-profile'),
    path('transactions/', views.viewTransactions, name='main-transactions')
]