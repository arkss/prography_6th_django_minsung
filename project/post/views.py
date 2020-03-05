from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Post
from .serializers import PostSerializer
from .paginations import PostPageNumberPagination
from config.permissions import IsOwnerOnly


class PostView(APIView):
    pagination_class = PostPageNumberPagination
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(
                self.serializer_class(page, many=True).data)

        else:
            serializer = self.serializer_class(page, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request, *args, **kwargs):
        '''
        {
            "post": {
                "title": "첫번째 글",
                "description": "첫번째 글의 내용"
            }
        }
        '''
        data = request.data['post']

        FK = dict()
        FK['profile'] = request.user
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save(FK=FK)
        return Response({
            'response': 'success',
            'message': 'post가 성공적으로 생성되었습니다.'
        })

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class PostDetailView(APIView):
    permission_classes = [IsOwnerOnly]

    def get_object(self, post_id):
        post = Post.objects.get(id=post_id)
        self.check_object_permissions(self.request, post)
        return post

    def get(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        return Response({
            'data': serializer.data
        })

    def put(self, request, post_id):
        '''
        {
            "content": "스마일 세탁소 사랑해요!"
        }
        '''

        post = self.get_object(post_id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response({
            'data': serializer.data
        })

    def delete(self, request, post_id):
        post = self.get_object(post_id)
        post.delete()
        return Response({
            'response': 'success',
            'message': 'post가 성공적으로 삭제되었습니다.'
        })
