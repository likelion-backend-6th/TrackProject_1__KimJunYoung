from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.models import User
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

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

    @action(detail=False, methods=["get"], url_name="my_post")
    def my_post(self, request: Request, *args, **kwargs):
        user = request.user
        obj = Post.objects.filter(owner=user)
        serializer = PostSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_name="following_post")
    def following_post(self, request: Request, *args, **kwargs):
        user = request.user
        follow = Follow.objects.filter(follower=user)
        serializer = FollowSerializer(follow, many=True)
        following_list = []
        for data in serializer.data:
            following_list.append(data["following"])

        obj = Post.objects.filter(owner__in=following_list)
        serializer = PostSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        title = request.data.get("title")
        body = request.data.get("body")
        owner = request.user
        post = Post.objects.create(title=title, body=body, owner=owner)
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request: Request, *args, **kwargs):
        user = request.user
        post: Post = self.get_object()
        if not post.access_by_post(user):
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized")

        return super().destroy(request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs):
        user = request.user
        post: Post = self.get_object()
        if not post.access_by_post(user):
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized")
        return super().update(request, *args, **kwargs)

    @extend_schema(deprecated=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Deprecated API")


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
