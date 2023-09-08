from rest_framework import serializers
from blog.models import Post, Follow
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("owner", "created_at", "updated_at")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]
        read_only_fields = ("username",)
