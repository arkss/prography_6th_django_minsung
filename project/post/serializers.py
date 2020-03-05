from rest_framework import serializers as sz
from .models import Post


class PostSerializer(sz.ModelSerializer):
    username = sz.SerializerMethodField()

    def get_username(self, post):
        return post.profile.username

    def create(self, validated_data):
        FK = validated_data.pop('FK')
        post = Post(
            **validated_data
        )
        post.profile = FK['profile']
        post.save()
        return post

    class Meta:
        model = Post
        fields = [
            'id', 'username', 'title', 'description', 'created_at'
        ]
