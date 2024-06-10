from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .modelsAPI import TaskAPI
from .forms import TaskForm
from .serializers import UserSerializer

class SignUpView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'success': True, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class TaskListView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        tasks = TaskAPI.objects.filter(user=request.user)
        uncompleted_tasks = tasks.filter(completed=False)
        completed_tasks = tasks.filter(completed=True)
        return Response({
            'tasks': [task.to_dict() for task in tasks],
            'uncompleted_tasks': [task.to_dict() for task in uncompleted_tasks],
            'completed_tasks': [task.to_dict() for task in completed_tasks],
        })

class TaskEditView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, task_id):
        task = get_object_or_404(TaskAPI, id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return Response({'success': True, 'task': task.to_dict()}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

class TaskDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        try:
            task = get_object_or_404(TaskAPI, id=task_id)
            task.delete()
            return Response({'success': True})
        except TaskAPI.DoesNotExist:
            return Response({'success': False, 'error': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
class AddTaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = TaskForm(request.data)
        if form.is_valid():
            task = form.save(commit=False)
            print(type(task))
            task.user = request.user
            task.save()
            return Response({'success': True, 'task': task.to_dict()}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

class UpdateTaskStatusView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        task_id = request.data.get('task_id')
        completed = request.data.get('completed') == 'true'

        try:
            task = TaskAPI.objects.get(id=task_id, user=request.user)
            task.completed = completed
            task.save()
            return Response({'success': True})
        except TaskAPI.DoesNotExist:
            return Response({'success': False, 'error': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)