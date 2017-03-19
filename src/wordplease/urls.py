"""wordplease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from blog.api import PostListAPI, NewPostAPI, PostDetailAPI, BlogListAPI
from blog.views import post_list, user_posts, blog_list, post_detail, NewPostView
from users.api import UsersAPI, UserDetailAPI
from users.views import LoginView, logout, UserView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', post_list, name="post_list"),
    url(r'^blogs/$', blog_list, name="blog_list"),
    url(r'^blogs/(?P<user_name>[a-zA-Z0-9]+)/$', user_posts, name="user_posts"),
    url(r'^blogs/(?P<user_name>[a-zA-Z0-9]+)/(?P<post_pk>[0-9]+)/$', post_detail, name="post_detail"),
    url(r'^new-post/$', NewPostView.as_view(), name="post_new"),

    #Users
    url(r'^login$', LoginView.as_view(), name="login"),
    url(r'^logout$', logout, name="logout"),
    url(r'^signup$', UserView.as_view(), name="signup"),

    #API Users. Me permiten. La primera consultar los usuarios, y la segunda ver el detalle, borrar o actualizar el usuario con ese id.
    url(r'^api/1.0/users/$', UsersAPI.as_view(), name="users_api"),
    url(r'^api/1.0/users/(?P<pk>[0-9]+)/$', UserDetailAPI.as_view(), name="user_detail"),

    #API Blogs. Endpoints para listado de blogs, leer articulos de un blog y para crear, modificar y borrar posts.
    url(r'^api/1.0/blogs/$', BlogListAPI.as_view(), name="bloglist_api"),
    url(r'^api/1.0/blogs/(?P<pk>[0-9]+)/$', PostListAPI.as_view(), name="postlist_api"),
    url(r'^api/1.0/newposts/$', NewPostAPI.as_view(), name="newpost_api"),
    url(r'^api/1.0/postdetail/(?P<pk>[0-9]+)/$', PostDetailAPI.as_view(), name="post_detail")
]
