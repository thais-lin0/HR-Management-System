"""
URL configuration for hrproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from funcionarios import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path('signup/', views.signup, name='signup'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # Home
    path('home/', views.home, name='home'),

    # Home
    path('', views.home, name='home'),

    # Sobre
    path('sobre/', views.sobre, name='sobre'),

    # Funcionarios
    path('funcionarios/', views.funcionarios, name='funcionarios'),

    # Aceitar ou Negar Férias
    path('aceiteferias/', views.aceiteferias, name='aceiteferias'),
    
    # Solicitar Férias
    path('ferias/', views.ferias, name='ferias'),

    # Status Férias
    path('status/', views.status, name='status'),
    
    # staff_only_view
    path('staff/', views.staff_only_view, name='staff'),

    # Bater ponto
    path('ponto/', views.ponto, name='ponto'),

    # Dados do funcionário
    path('dados/', views.dados, name='dados'),

    # Reset da senha
    path('reset_password/', views.reset_password, name='reset_password'),
]
