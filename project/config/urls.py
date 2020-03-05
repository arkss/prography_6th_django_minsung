from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myauth/', include('myauth.urls')),
    path('post/', include('post.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
