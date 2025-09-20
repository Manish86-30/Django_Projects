from django.urls import path
from .import views


urlpatterns = [
    path('', views.read_data, name='read'),
    path('create/', views.create_data, name='create_data'),
    path('update/<int:id>/', views.update_data, name='update_data'),
    path('delete/<int:id>/', views.delete_data, name='delete_data'),
    path('export_excel/', views.export_excel, name='export_excel'),
    path('delete-all/', views.delete_all, name='all_delete'),
]
