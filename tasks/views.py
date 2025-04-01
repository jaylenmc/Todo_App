from rest_framework.response import Response
from django.conf import settings
from .models import Task
from authentication.models import AppUser
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from .serializer import taskSerializer
from rest_framework import status

@login_required
@api_view(['POST'])
def newTask(request):
    task_user = AppUser.objects.filter(email=request.data.get('email')).first()
    task_title = request.data.get('title')
    task_description = request.data.get('description', 'No description provided')
    new_task = Task.objects.create(
        user = task_user,
        title = task_title,
        description = task_description
    )
    new_task.save()

    serilizer = taskSerializer(new_task)

    return Response(serilizer.data, status=200)

@login_required
@api_view(['POST'])
def editTask(request):
    task_user = AppUser.objects.filter(email=request.data.get('email')).first()
    new_title = request.data.get('title')
    new_description = request.data.get('description')
    task_id = request.data.get('id')

    updating_task = task_user.tasks.filter(id=task_id).first()
    updating_task.title = new_title
    updating_task.description = new_description
    updating_task.save()

    serialized = taskSerializer(updating_task)

    return Response(serialized.data)

@login_required
@api_view(['DELETE'])
def deleteTask(request, task_id):
    user = AppUser.objects.filter(email=request.user).first()
    task = user.tasks.filter(id=task_id).first()
    if not task:
        return Response({"Error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    task.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)