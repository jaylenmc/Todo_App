from django.shortcuts import render, HttpResponse
from django.conf import settings

def home(request):
    print(f'User: {request.user}')
    print(f'Session ID: {request.session.session_key}')

    context = {
        'login_url': f'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&redirect_uri={settings.REDIRECT_URI}&scope=openid%20profile%20email&client_id={settings.GOOGLE_CLIENT_ID}'
    }
    return render(request, 'tasks/home.html', context)

def userTasks(request):
    return render(request, 'tasks/todo.html')