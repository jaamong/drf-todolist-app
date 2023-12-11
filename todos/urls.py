from django.urls import path

from .views import ListCreateTodosAPIView

urlpatterns = [
    path('', ListCreateTodosAPIView.as_view(), name='create-list-todo'),
    # path('create', CreateTodoAPIView.as_view(), name='create-todo'),
    # path('list', ListTodoAPIView.as_view(), name='list-todo'),
]
