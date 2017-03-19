from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponse, request
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from blog.forms import PostForm
from blog.models import Post


def post_list(request):
    """
    Recupera todos los post de todos los usuarios y el campo relacionado owner
    """

    posts = Post.objects.select_related("owner").all().order_by('-created_at').filter(post_published="PUB")

    context = {
        "posts": posts
    }

    return render(request, "blog/home.html", context)


def blog_list(request):

    """
    :param request: HttpRequest
    :return: HttpResponse
    """
    blogs = User.objects.all()

    context = {
        "blogs": blogs
    }

    return render(request, "blog/blogs.html", context)


def user_posts(request, user_name):
    """
    Recuper los post del usuario que se le pasa como parametro
    :param request: HttpRequest
    :param user_name: username del usuario del que queremos los post
    :return: HttpResponse
        try:
        posts = User.objects.get(username=user_name)
    except User.DoesNotExist:
        return HttpResponseNotFound("No se ha encontrado dicho usuario")
    except User.MultipleObjectsReturned:
        return HttpResponse("Se han encontrado varios usuarios con ese username", status=300)
    """

    try:
        #Intento Almacenar el objeto usuario cuyo username es igual a user_name que lo paso como parametro desde urls.py
        user_blog = User.objects.get(username=user_name)
    except User.DoesNotExist:
        return HttpResponseNotFound("No se ha encontrado dicho usuario")
    except User.MultipleObjectsReturned:
        return HttpResponse("Se han encontrado varios usuarios con ese username", status=300)

    #Si he encontrado el usuario con ese username almaceno todos sus objectos posts en la variable posts

    posts = user_blog.owned_posts.all().order_by('-created_at')

    context = {
        "posts": posts,
        "user": user_blog
    }

    return render(request, "blog/user_post_list.html", context)


def post_detail(request, user_name, post_pk):
    """
    Capturamos en la url en la variable post_pk el id del post introducido por el usuario o desde un enlace, para mostrar el detalle de ese post
    :param request: HttpRequest
    :param post_pk: variable que contiene el id y que comprobare que exista
    :return: HttpResponse
    """

    try:
        user_blog = User.objects.get(username=user_name)
        detail_post = user_blog.owned_posts.get(pk=post_pk)
    except User.DoesNotExist:
        return HttpResponseNotFound("No se ha encontrado dicho usuario")
    except Post.DoesNotExist:
        return HttpResponseNotFound("No se ha encontrado dicho post")
    except User.MultipleObjectsReturned:
        return HttpResponse("Se han encontrado varios usuarios con ese username", status=300)
    except Post.MultipleObjectsReturned:
        return HttpResponse("Se han encontrado varios post con ese id", status=300)

    context = {
        "detail_post": detail_post
    }

    return render(request, "blog/post_detail.html", context)


class NewPostView(View):

    @method_decorator(login_required)
    def get(self, request):

        form = PostForm()

        context = {
            "form": form
        }

        return render(request, 'blog/new_post.html', context)

    @method_decorator(login_required)
    def post(self, request):

        post_with_user = Post(owner=request.user)
        form = PostForm(request.POST, instance=post_with_user)
        if form.is_valid():
            new_post = form.save()
            message = 'Post creado con éxito'
            form = PostForm()
        else:
            message = "Se ha producido un error"

        context = {
            "form": form,
            "message": message
        }

        return render(request, "blog/new_post.html", context)