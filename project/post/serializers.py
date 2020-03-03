from rest_framework import serializers as sz
from .models import Post


class PostSerializer(sz.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'description', 'created_at'
        ]
