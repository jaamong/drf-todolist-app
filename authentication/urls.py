from django.urls import path

from authentication import views

urlpatterns = [
    path('register', views.RegisterAPIVIew.as_view(), name='register'),
]
