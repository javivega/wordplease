from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework import serializers

from blog.models import Post

class CategoriesSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    category_name = serializers.CharField()
    category_short = serializers.CharField()


class UrlField(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'user_name': obj.get('username')
        }
        return reverse(view_name, kwargs=url_kwargs, request=request)


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["title", "post_img", "post_intro", "created_at"]


class NewPostSerializer(serializers.ModelSerializer):
    post_category = CategoriesSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('owner',)


class BlogListSerializer(serializers.ModelSerializer):
    url_blog = UrlField(view_name='user_posts', read_only=True)

    class Meta:
        model = User
        fields = ("id", 'username', 'url_blog')



