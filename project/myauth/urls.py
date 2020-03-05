from django.urls import path
from . import views

app_name = 'myauth'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('logout/', views.logout, name="logout"),
    path('sign_up/', views.CreateProfileView.as_view(), name="sign_up"),
    path('profile_activate/<str:uuid>/',
         views.profile_activate, name="profile_activate"),
]
