# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import UserPermission
from users.serializers import UserSerializer, UsersListSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import mixins
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from users import emails
from django.conf import settings


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
        if(request.data.get('email') and User.objects.filter(email=request.data['email']).exists()):
            return Response({'email_error': 'This email has been registered for other user.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            data_to_return = serializer.data

            return Response(data_to_return, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Recovery(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        if(request.data.get('email') and User.objects.filter(email=request.data['email']).exists()):
            user = User.objects.filter(email=request.data['email'])[0]
            password = get_random_string(length=10)
            user.set_password(password)
            user.save()

            send_mail(
                emails.PASSWORD_RECOVERY_SUBJECT,
                emails.PASSWORD_RECOVERY_BODY % {'user': user.username,
                                                 'password': password},
                settings.WELLCODERS_RECOVERY_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
        return Response({'success': 'If this email is registered, it will receive a new password.'}, status=status.HTTP_200_OK)
