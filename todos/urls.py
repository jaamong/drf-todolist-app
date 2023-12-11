from django.urls import path

from .views import ListCreateTodosAPIView, TodoDetailAPIView

urlpatterns = [
    path('', ListCreateTodosAPIView.as_view(), name='create-list-todo'),
    # path('create', CreateTodoAPIView.as_view(), name='create-todo'),
    # path('list', ListTodoAPIView.as_view(), name='list-todo'),
    path('<int:id>', TodoDetailAPIView.as_view(), name='detail-todo'),
]
