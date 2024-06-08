from .views import SignUpView
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('', views.task_list, name='task_list'),  
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update_task_status/', views.update_task_status, name='update_task_status'),
]
