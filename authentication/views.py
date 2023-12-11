from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

import authentication.jwt
from authentication.serializers import RegisterSerializer, LoginSerializer


class AuthUserAPIView(GenericAPIView):
    """
    for this to work, throw an error when the user is not authenticated.
    we need to have permission set up on this view.
    """
    permission_classes = [permissions.IsAuthenticated,]  # user should have a token
    authentication_classes = [authentication.jwt.JWTAuthentication,]

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response({'user': serializer.data})


class RegisterAPIVIew(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():  # if the data we sent to the serializer is valid,
            serializer.save()  # then save
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        # when a user doesn't send these keys, gate will throw a key error
        # so first, what you want to do now is do 'None' here
        email = request.data.get('email', None)  # <-- None
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user:  # if user, then log them in. and send them token.
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'invalid credentials. try again'},  # authentication is failed
                        status=status.HTTP_401_UNAUTHORIZED)
