from django.urls import path
from .import views



urlpatterns = [
    path('register/', views.Register_Page, name='register'),
    path('login/', views.Login_Page, name='login'),
    path('logout/', views.Logout_Page, name='logout'),
    path("change/", views.change_password, name="change"),
    path('', views.Home_Page, name='home'),


]
