from django.urls import path, include

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('tasks/', include('tasks.urls'))
    # path('tasks/', views.userTasks, name='userTasks'),
    # path('tasks/delete/<int:task_id>/',views.deleteTask, name='deleteTask' ),
]