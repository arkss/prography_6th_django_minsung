from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


class PostView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()

        serializer = PostSerializer(queryset, many=True)
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
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
        return Response({
            'response': 'success',
            'message': 'post가 성공적으로 생성되었습니다.'
        })


class PostDetailView(APIView):
    def get_object(self, post_id):
        post = Post.objects.get(id=post_id)
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
