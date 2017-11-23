from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostSerializer
from django.conf.urls import url

class PostPagination(PageNumberPagination):
    page_size = 10


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination

urlpatterns = [
    url(r'^posts\.json/$', PostListAPIView.as_view(), name='post_list'),
]