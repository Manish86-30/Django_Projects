from django.urls import path
from .import views


urlpatterns = [
    path('', views.homeview.as_view(), name='home'),
    path('article/<int:pk>', views.articleview.as_view(), name='details'),
    path('add/', views.Create_Post.as_view(), name='add_post'),
    path('update/<int:pk>', views.Update_view.as_view(), name='update'),
    path('delete/<int:pk>/remove/', views.Delete_view.as_view(), name='delete'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('logout/', views.User_logout.as_view(), name='logout'),
    path('login/', views.User_login.as_view(), name='login'),
    path('dash/', views.User_dashboard.as_view(), name='dash'),
    path('', views.TaskList.as_view(), name='tasks'),    
]
