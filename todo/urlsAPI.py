from django.contrib.auth import views as auth_views
from django.urls import path, include
from .viewsAPI import SignUpView, TaskListView, TaskEditView, TaskDeleteView, AddTaskView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/add/', AddTaskView.as_view(), name='add_task'),
    path('tasks/edit/', TaskEditView.as_view(), name='task_edit'),
    path('tasks/delete/', TaskDeleteView.as_view(), name='task_delete'),
]