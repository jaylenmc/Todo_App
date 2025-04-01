from django.urls import path
from . import views

urlpatterns = [
    path('newtask/', views.newTask),
    path('edit/', views.editTask),
    path('delete/<int:task_id>', views.deleteTask)
]
