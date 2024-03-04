from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework import status
from rockerboy_backend_app.settings import SECRET_KEY

import datetime
import jwt

from .serializers import CustomUserSerializer
from .models import CustomUser

from django.shortcuts import get_object_or_404

from .utils import get_auth_token, get_user_from_request


class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    def post(self, request):
        req_username = request.data['username']
        req_password = request.data['password']

        user = get_object_or_404(CustomUser, username=req_username)

        if not user.check_password(req_password):
            return AuthenticationFailed('Username and password do not match!')
        
        payload = {
            'id' : user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return Response({
            "access_token" : token
        })


class UserView(APIView):
    def get(self, request):
        user_data = get_user_from_request(request)
        return Response(user_data)

