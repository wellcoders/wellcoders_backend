# -*- coding: utf-8 -*-
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin
from posts.models import Post
from posts.serializers import PostSerializer, Pagination
from django.utils import timezone

class PostsAPI(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.select_related().filter(publish_date__lte=timezone.now(), status=Post.PUBLISHED).all().order_by('-publish_date')
    pagination_class = Pagination
