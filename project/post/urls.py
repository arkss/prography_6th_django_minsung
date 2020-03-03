from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.PostView.as_view(), name="post"),
    path('<int:post_id>/', views.PostDetailView.as_view(), name="post_detail"),
]
