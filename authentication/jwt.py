import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication

from authentication.models import User


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')  # string token (included 'Bearer')
        auth_token = auth_data.split(" ")  # this split returns list format (length == 2)

        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed('token not valid')

        token = auth_token[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            username = payload['username']
            user = User.objects.get(username=username)

            return user, token

        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed('token is expired, login again.')
        except jwt.DecodeError as e:
            raise exceptions.AuthenticationFailed('token is invalid.')
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed('No such user')

        return super().authenticate(request)
