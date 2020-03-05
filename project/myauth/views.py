from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Profile
from .serializers import ProfileSerializer
# mail 인증
from uuid import uuid4
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
# Create your views here.


class CreateProfileView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        {
            "profile": {
                "username": "rkdalstjd1",
                "password": "password1",
                "email": "rkdalstjd9@naver.com"
            }
        }
        '''
        data = request.data.get('profile')
        if data is None:
            return Response({
                'response': 'error',
                'message': 'profile 값이 없습니다.'
            })

        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            profile = serializer.save()
        else:
            return Response({
                'response': 'error',
                'message': serializer.errors
            })
        uuid = urlsafe_base64_encode(force_bytes(profile.id)).encode().decode()
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
        email_result = email.send()
        if email_result == 1:
            return Response({
                'response': 'success',
                'message': 'profile이 성공적으로 생성되었습니다. 이메일을 확인해주세요.'
            })
        else:
            return Response({
                'response': 'error',
                'message': '이메일 발송에 실패하였습니다.'
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
        data = request.data.get('profile')
        if data is None:
            return Response({
                'response' 'error',
                'message': 'profile 값이 없습니다.'
            })
        username = data['username']
        password = data['password']

        profile = auth.authenticate(
            request, username=username, password=password
        )
        if profile is None:
            return Response({
                'response': 'error',
                'message': '해당 유저가 존재하지 않습니다.'
            })

        if profile.status == '0':
            return Response({
                'response': 'error',
                'message': '해당 계정은 권한이 없습니다. (이메일 인증 필요)'
            })

        elif profile.status == '1':
            auth.login(request, profile)
            return Response({
                'response': 'success',
                'message': '로그인이 성공하였습니다.'
            })


@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    auth.logout(request)
    return Response({
        'response': 'success',
        'message': '로그아웃 요청에 성공하였습니다.'
    })


def profile_activate(request, uuid):
    profile_id = force_text(urlsafe_base64_decode(uuid))
    try:
        profile = Profile.objects.get(id=profile_id)
    except ObjectDoesNotExist:
        return Response({
            'response': 'error',
            'message': '해당 profile이 존재하지 않습니다.'
        })
    profile.status = '1'
    profile.save()
    return HttpResponse("이메일 인증에 성공하였습니다.")
