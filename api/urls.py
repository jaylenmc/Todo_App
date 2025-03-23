from django.urls import path
from . import views

urlpatterns = [
    path('goolgle/auth', views.person),
    path('logout/', views.loggingOut, name='logout')
]

app_name = 'api'