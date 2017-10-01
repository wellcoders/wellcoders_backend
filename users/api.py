# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import UserPermission
from users.serializers import UserSerializer, UsersListSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import mixins


class UserAPI(mixins.ListModelMixin,
              mixins.RetrieveModelMixin,
              mixins.UpdateModelMixin,
              mixins.DestroyModelMixin,
              viewsets.GenericViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('username')
    ordering = ('username')

    permission_classes = (UserPermission,)

    def get_serializer_class(self):
        return UsersListSerializer if self.action == "list" else UserSerializer


class Register(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            data_to_return = serializer.data
#            data_to_return.pop('password')

            return Response(data_to_return, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





