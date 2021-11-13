from django.urls import path
from .views import list_task, retrieve_task, create_task

urlpatterns = [
    path('list/', list_task, name='list-view'),
    path('retrieve/<int:task_id>', retrieve_task, name='retrieve-view'),
    path('create/', create_task, name='create-view')
]
