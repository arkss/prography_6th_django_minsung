from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password
        )
        user.role = "10"
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    STATUS_CHOICES = (
        ('0', '가입대기'),
        ('1', '가입활성화'),
        ('8', '블랙리스트'),
        ('9', '탈퇴')
    )

    ROLE_CHOICES = (
        ('0', '일반 유저'),
        ('10', '관리자')
    )

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=50)
    status = models.CharField(
        max_length=2, default='0', choices=STATUS_CHOICES)
    role = models.CharField(max_length=2, default='0', choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_staff(self):
        return self.role == '10'

    @property
    def is_superuser(self):
        return self.role == '10'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
