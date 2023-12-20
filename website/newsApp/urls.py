from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('loginIndex/',views.loginIndex, name='loginIndex'),
    path('loginIndex/logout/',views.logout, name='logout'),
    path('recherche',views.index,name='recherche'),

]