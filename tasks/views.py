from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Task, AppUser
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

@login_required
@api_view(['POST'])
def userTasks(request):
    user = request.data.get('email')
    list_items = Task.objects.all().filter(user=user)
    serilizer = taskSerializer(list_items, many=True)
    context = {
        'form': form,
        'tasks': serilizer.data,
    }

    return render(request, 'tasks/todo.html', context=context)

def deleteTask(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()

    return redirect('/tasks/')