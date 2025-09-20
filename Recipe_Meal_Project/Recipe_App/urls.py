from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('logout/', views.custom_logout, name="logout"),
    path('pdf/', views.pdf , name='pdf'),
    path('admin/', admin.site.urls),
    path('login/' , views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    
    path('', views.recipe, name='recipe'),
    path('update_recipe/<int:id>', views.update_recipe, name='recipe'),
    path('delete_recipe/<int:id>', views.delete_recipe, name='delete_recipe'),
]