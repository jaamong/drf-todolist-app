from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

import authentication.jwt
from .models import Todo
from .serializers import TodoSerializer


class ListCreateTodosAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [authentication.jwt.JWTAuthentication]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)


# class CreateTodoAPIView(CreateAPIView):
#     serializer_class = TodoSerializer
#     permission_classes = [IsAuthenticated, ]
#     authentication_classes = [authentication.jwt.JWTAuthentication]
#
#     def perform_create(self, serializer):
#         return serializer.save(owner=self.request.user)
#
#
# class ListTodoAPIView(ListAPIView):
#     serializer_class = TodoSerializer
#     # queryset = Todo.objects.all()
#     permission_classes = [IsAuthenticated, ]
#     authentication_classes = [authentication.jwt.JWTAuthentication]
#
#     def get_queryset(self):
#         return Todo.objects.filter(owner=self.request.user)
