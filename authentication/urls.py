from django.urls import path
from . import views

urlpatterns = [
    path('check/', views.authorization_code),
    path('google/', views.person),
    path('logout/', views.loggingOut, name='logout'),
    # path('test/', views.test),
]
