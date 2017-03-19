from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import request
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.models import Post
from blog.permissions import ArticlePermission
from blog.serializers import BlogSerializer, NewPostSerializer, BlogListSerializer





class BlogListAPI(ListAPIView):
    """Lista los blogs de la plataforma"""
    serializer_class = BlogListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username',)
    ordering_fields = ('username',)
    queryset = User.objects.all().values('id', 'username')


class PostListAPI(ListAPIView):
    """Lista los post del blog de un usuario"""

    serializer_class = BlogSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'post_intro', 'post_body', 'post_category')
    ordering_fields = ('title', 'created_at')

    def get_queryset(self):
        """Si el usuario es el propietario o admin le mostramos todos los posts y si no solo los publicados"""
        if str(self.request.user.id) == self.kwargs.get('pk', '') or self.request.user.is_superuser:
            filtersposts = Post.objects.select_related().filter(owner__id=self.kwargs.get('pk', '')).order_by('-created_at')
        else:
            filtersposts = Post.objects.select_related().filter(owner__id=self.kwargs.get('pk', '')).order_by('-created_at').filter(post_published="PUB")
        return filtersposts


class NewPostAPI(APIView):

    def post(self, request):
        """Me permite crear nuevos posts, metodo get no permitido"""
        serializer = NewPostSerializer(data=request.data)
        permission_classes = (IsAuthenticated,)

        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            new_post = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    """Recupera, actualiza y borra posts"""
    queryset = Post.objects.all().select_related()
    permission_classes = (ArticlePermission,)
    serializer_class = NewPostSerializer





