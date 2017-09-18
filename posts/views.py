from posts.models import Post
from posts.serializers import PostListSerializer
from rest_framework import generics, permissions


class PostList(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
