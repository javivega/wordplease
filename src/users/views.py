from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LoginForm, UserForm


class LoginView(View):

    def get(self, request):
        """Presenta el formulario de login a un usuario"""

        context = {
            "form": LoginForm()
        }
        return render(request, 'login.html', context)

    def post(self, request):
        """Codigo qu ese ejecuta cuando la peticion es post"""

        form = LoginForm(request.POST)
        context = dict()
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)
                url = request.GET.get('next', 'post_list')
                return redirect(url)
            else:
                context["error"] = "Wrong username or password"

        context["form"] = form
        return render(request, 'login.html', context)


def logout(request):
    """
    hace logout del usuario
    :param request:
    :return:
    """
    django_logout(request)
    return redirect('login')


class UserView(View):

    def get(self, request):
        form = UserForm()
        context = {
            "form": form
        }
        return render(request, 'register.html', context)

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('post_list')
        else:
            message = "Se ha producido un error"

        context = {
            "form": form,
            "message": message
        }

        return render(request, 'register.html', context)

