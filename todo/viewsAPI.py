from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Task
from .forms import TaskForm
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.core.exceptions import FieldError


class SignUpView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'success': True, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class TaskListView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, payload):
        filter = payload.data.get('filters', {})
        tasks = Task.objects.filter(**filter)
        ser = TaskSerializer(tasks, many=True)
        return Response({
            'tasks': ser.data,
        })

class TaskEditView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, payload):        
        task_id = payload.data.get('task_id')
        request = payload.data.get('request')
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(request, instance=task)
        if form.is_valid():
            form.save()
            return Response({'success': True, 'task': model_to_dict(task)}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

class TaskDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, payload):
        task_id = payload.data.get('task_id')
        try:
            task = get_object_or_404(Task, id=task_id)
            task.delete()
            return Response({'success': True})
        except Task.DoesNotExist:
            return Response({'success': False, 'error': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
class AddTaskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, payload):
        username = payload.data.get('username')
        request = payload.data.get('request')
        form = TaskForm(request)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = User.objects.get(username=username)
            task.save()
            return Response({'success': True, 'task': model_to_dict(task)}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

class UpdateTaskStatusView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, payload):
        task_id = payload.data.get('task_id')
        completed = payload.data.get('completed') == 'true'

        try:
            Task.objects.filter(id=task_id).update(completed=completed)
            return Response({'success': True})
        except Task.DoesNotExist:
            return Response({'success': False, 'error': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)