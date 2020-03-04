from django.urls import path
from . import views

app_name = 'myauth'

urlpatterns = [
    path('login/', views.CreateProfileView.as_view(), name="login"),
    path('sign_up/', views.UserLoginView.as_view(), name="sign_up"),
]
