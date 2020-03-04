from django.contrib.auth.hashers import check_password
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Profile
# mail 인증
from uuid import uuid4
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your views here.


class CreateProfileView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        {
            "profile": {
                "username": "rkdalstjd1",
                "password": "password1",
                "email": "rkdalstjd9@naver.com",
            }
        }
        '''
        data = request.data['profile']
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            profile = serializer.save()

        uuid = uuid4()
        current_site = get_current_site(request)
        message = render_to_string(
            'myauth/user_activate_email.html',
            {
                'domain': current_site.domain,
                'uuid': uuid
            }
        )
        mail_subject = "회원가입 인증 메일입니다."
        user_email = profile.email
        email = EmailMessage(mail_subject, message, to=[user_email])
        return Response({
            'response': 'success',
            'message': 'profile이 성공적으로 생성되었습니다. 이메일을 확인해주세요.'
        })


class UserLoginView(APIView):
    def post(self, request, *args, **kargs):
        '''
        {
            "profile": {
                "username": "rkdalstjd1",
                "password": "password1"
            }
        }
        '''
        data = request.data['profile']
        username = data['username']
        password = data['password']

        profile = auth.autheticate(
            request, username=username, password=password
        )

        if profile.status == '0':
            return Response({
                'response': 'error',
                'message': '해당 계정은 권한이 없습니다. (이메일 인증 필요)'
            })

        elif profile.status == '1':
            auth.login(reques, profile)
            return Response({
                'response': 'success',
                'message': '로그인이 성공하였습니다.'
            })


@api_view(['GET', ])
def logout(request):
    auth.logout(request)
    return Response({
        'response': 'success',
        'message': '로그아웃 요청에 성공하였습니다.'
    })


def profile_activate(request, uuid):
    pass
