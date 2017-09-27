# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.serializers import PostSerializer
from users.serializers import UserSerializer
from posts.models import Post


class Register(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            data_to_return = serializer.data
            data_to_return.pop('password')

            return Response(data_to_return, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





