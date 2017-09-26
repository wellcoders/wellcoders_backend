from posts.models import Post
from posts.serializers import PostListSerializer
from rest_framework import generics, permissions
from users.serializers import UserDetailSerializer


class PostList(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    owner = UserDetailSerializer()

    model = Post
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [
        permissions.AllowAny
    ]