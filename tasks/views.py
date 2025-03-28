from django.shortcuts import render, HttpResponse
from django.conf import settings
from .models import Task, AppUser
from .forms import TaskForm
from api.serializers import taskSerializer, UserSerializer
from django.contrib.auth.decorators import login_required

def home(request):
    print(f'User: {request.user}')
    print(f'Session ID: {request.session.session_key}')

    context = {
        'login_url': f'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&redirect_uri={settings.REDIRECT_URI}&scope=openid%20profile%20email&client_id={settings.GOOGLE_CLIENT_ID}'
    }
    return render(request, 'tasks/home.html', context)

@login_required
def userTasks(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()

        return render(request, 'tasks/todo.html')
    else:
        form = TaskForm()

    user = AppUser.objects.all().filter(email=request.user.email).first()
    person = UserSerializer(user)
    list_items = Task.objects.all().filter(id=person.data['id'])
    serilizer = taskSerializer(list_items, many=True)
    print(f"Here: {serilizer.data}")
    context = {
        'form': form,
        'tasks': serilizer.data,
    }

    return render(request, 'tasks/todo.html', context=context)