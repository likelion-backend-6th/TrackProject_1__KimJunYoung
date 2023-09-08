from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.models import User
from rest_framework.decorators import action

from .models import Post, Follow
from .serializers import (
    PostSerializer,
    FollowSerializer,
    UserSerializer,
    FollowerSerializer,
    FollowingSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request: Request, *args, **kwargs):
        title = request.data.get("title")
        body = request.data.get("body")
        owner = request.user
        post = Post.objects.create(title=title, body=body, owner=owner)
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, *args, **kwargs):
        user = request.user
        post: Post = self.get_object()
        if not post.access_by_post(user):
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized")
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        post: Post = self.get_object()
        if not post.access_by_post(user):
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized")

        return super().destroy(request, *args, **kwargs)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request: Request, *args, **kwargs):
        obj = User.objects.exclude(username=request.user)
        serializer = UserSerializer(obj, many=True)
        return Response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    @action(detail=False, methods=["get"], url_name="follower")
    def follower(self, request: Request, *args, **kwargs):
        follower = request.user
        obj = Follow.objects.filter(follower=follower)
        serializer = FollowerSerializer(obj, many=True)
        for data in serializer.data:
            data["following"] = User.objects.get(id=data["following"]).username

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_name="following")
    def following(self, request: Request, *args, **kwargs):
        following = request.user
        obj = Follow.objects.filter(following=following)
        serializer = FollowingSerializer(obj, many=True)
        for data in serializer.data:
            data["follower"] = User.objects.get(id=data["follower"]).username

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        follower = request.user
        following = User.objects.get(id=request.data.get("following"))
        follow, created = Follow.objects.get_or_create(
            follower=follower, following=following
        )
        serializer = FollowSerializer(follow)
        if not created:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request: Request, *args, **kwargs):
        follower = request.user
        following = User.objects.get(username=kwargs["username"])
        follow = Follow.objects.get(follower=follower, following=following)
        follow.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
