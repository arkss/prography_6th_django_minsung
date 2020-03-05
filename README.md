# prography_6th_django_minsung

### 기술스택

Python==3.7.1

Django==3.0.3

djangorestframework==3.11.0

MySQL==8.0.19



### API 문서

#### myauth

##### myauth/login/

* POST

  * 로그인

  * request body

    ```json
    {
      "profile": {
        "username": "rkdalstjd1",
        "password": "password1"
      }
    }
    ```



##### myauth/logout

* GET

  * 로그아웃

    



##### myauth/sign_up/

* POST

  * 회원가입

  * request body

    ``` json
    {
      "profile": {
        "username": "rkdalstjd1",
        "password": "password1",
        "email": "rkdalstjd9@naver.com"
      }
    }
    ```



#### post

##### post/

* GET

  * 글 목록 조회

  * response body

    ```json
    {
        "data": {
            "count": 4,
            "next": "http://127.0.0.1:8000/post/?page=2",
            "previous": null,
            "results": [
                {
                    "id": 5,
                    "username": "rkdalstjd2",
                    "title": "다섯번째 글",
                    "description": "다섯번째 글의 내용",
                    "created_at": "2020-03-05T06:48:59.917750Z"
                },
                {
                    "id": 4,
                    "username": "root",
                    "title": "네번째 글",
                    "description": "네번째 글의 내용",
                    "created_at": "2020-03-03T17:19:10.074762Z"
                }
            ]
        }
    }
    ```

    

* POST

  * 글 생성

  * request body

    ```json
    {
        "post": {
            "title": "첫번째 글",
            "description": "첫번째 글의 내용"
        }
    }
    ```

    

##### post/\<int:post_id>/

* GET

  * 글 세부 조회

  * response body

    ```json
    {
        "data": {
            "id": 5,
            "username": "rkdalstjd2",
            "title": "다섯번째 글",
            "description": "다섯번째 글의 내용",
            "created_at": "2020-03-05T06:48:59.917750Z"
        }
    }
    ```

    

* PUT

  * 글 수정

  * request body

    ```json
    {
      "title": "첫번째 글 수정"
    }
    ```

    

* DELETE

  * 글 삭제

    

### 기타 특이사항

* Profile 모델

  * 사용자 권한을 위해 Profile 모델 생성

  * `BaseUserManager` 를 통해 first name, last name 등 불필요한 필드 제거

  * 유저 권한 상태 status

    * 0 : 가입대기
    * 1 : 가입 활성화
    * 8 : 블랙 리스트
    * 9 : 탈퇴

  * 유저 역할 role

    * 0 : 일반유저
    * 10 : 관리자

    > 확장성을 위해 중간 숫자는 비워놓음



* email 인증
  * smtp를 이용한 이메일 발송
  * profile id를 암호화한 후 이메일에 첨부하여 해당 링크 클릭 시, 복호화하여 해당 profile 활성화



* permissions
  * django rest framework 기본 permissions인 `AllowAny`,  `IsAuthenticated` 외에 커스텀 permissions
  * `config/permissions` 에 `IsOwnerOnly` 
  * 작성자에게만 허용



* error handling

  여러 상황에 대한 에러 핸들링을 하고 있습니다.

  ```python
  # post/views.py
  
  post = self.get_object(post_id)
  if post is None:
    return Response({
      'response': 'error',
      'message': 'post값이 존재하지 않습니다.'
    })
  ```

  

* 배포

  http://rkdalstjd9.pythonanywhere.com/