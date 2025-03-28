from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse, redirect, render
import requests
from django.conf import settings
from tasks.models import AppUser
from django.contrib.auth import login, logout
from .serializers import UserSerializer

@api_view(['GET'])
def person(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    if not code or error:
        return Response("Missing code or there was an error", status=400)
    
    data = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.REDIRECT_URI,
        'code': code,
    }
    access_code_url = 'https://oauth2.googleapis.com/token'

    response = requests.post(access_code_url, data=data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
    else:
        return Response(f"Error getting access token: {response.text}", status=400)
    
    header = {
        'Authorization': f'Bearer {access_token}'
    }
    
    user_info = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers=header)

    if user_info.status_code == 200:
        user_email = user_info.json().get('email', 'No email provided')
        first_name = user_info.json().get('given_name', 'No name provided')

        user = AppUser.objects.filter(email=user_email).first()

        if user:    
            user.email = user_email
            user.name = first_name
            user.save()
        else:
            user = AppUser.objects.create(
                name=first_name,
                email=user_email
            )

        login(request, user)
        
    else:
        return Response(f"There was an error getting user info: {user_info.text}", status=400)

    serializer = UserSerializer(user)


    return render(request, 'tasks/home.html', context=serializer.data)

def loggingOut(request):
    logout(request)
    return redirect('/')