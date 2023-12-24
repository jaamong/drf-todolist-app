from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

import authentication.jwt
from .models import Todo
from .serializers import TodoSerializer


class ListCreateTodosAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [authentication.jwt.JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'title', 'desc', 'is_complete']
    search_fields = ['id', 'title', 'desc', 'is_complete']
    ordering_fields = ['id', 'title', 'desc', 'is_complete']

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


class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [authentication.jwt.JWTAuthentication]

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)
