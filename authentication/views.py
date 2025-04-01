from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import redirect
import requests
from django.conf import settings
from .models import AppUser
from django.contrib.auth import login, logout
from .serializers import UserSerializer
from django.utils import timezone
from datetime import timedelta

@api_view(['GET'])
def authorization_code(request):
    data = {"code": request.GET.get('code')}
    return Response(data, status=200)

@api_view(['POST'])
def person(request):
    code = request.data.get('code')
    error = request.data.get('error')

    if not code or error:
        return Response("Missing code or there was an error", status=400)
    
    data = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.REDIRECT_URI,
        'code': code,
        'access_type': 'offline',
    }
    access_code_url = 'https://oauth2.googleapis.com/token'
    response = requests.post(access_code_url, data=data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        token_expires_in = response.json().get('expires_in')
        expires_at = timezone.now() + timedelta(seconds=token_expires_in)
        token_refresh = response.json().get('refresh_token')
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
            user.expires_in = expires_at
            if not user.refresh_token:
                user.refresh_token = token_refresh
            user.save()
        else:
            user = AppUser.objects.create(
                name=first_name,
                email=user_email,
                expires_in=expires_at,
                refresh_token=token_refresh
            )

        login(request, user)
        
    else:
        return Response(f"There was an error getting user info: {user_info.text}", status=400)

    serializer = UserSerializer(user)


    return Response(serializer.data, status=200)

def loggingOut(request):
    logout(request)
    return redirect('/')

def refresh_access_token(refresh_token):
    token_refresh_url = 'https://oauth2.googleapis.com/token'
    data = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    try:
        response = requests.post(token_refresh_url, data=data)
        if response.status_code == 200:
            response_data = response.json()
            access_code = response_data.get('access_token')
            expires_in = response_data.get('expires_in')
            
            if access_code and expires_in:
                return access_code, expires_in
            else:
                raise Exception("Error: Missing access token or expires in")
        else:
            raise Exception(f"Error refreshing token:{response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")

# @api_view(['POST'])
# def test(request):
#     refresh_token = request.data.get('refresh_token')
#     current_time = timezone.now()
#     current_time += timedelta(hours=2)
#     expires_in_str = request.data.get('expires_in')
#     expires_in = datetime.fromisoformat(expires_in_str.replace("Z", "+00:00")).astimezone(pytz.utc)
#     print(current_time)
#     print(request.data.get('expires_in'))
#     if current_time > expires_in:
#         access_token, expires_in = refresh_access_token(refresh_token)
#         info = {
#             'access_token': access_token,
#             'expires_in': expires_in,
#         }

#         return Response(info, status=200)