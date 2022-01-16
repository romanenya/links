from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import random, string, reverse, validators
from .models import Link


class MainView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/account")
        else:
            return redirect('/sign_in')


class SignInView(View):
    template_name = "mainpage/sign_in.html"
    model = User

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return redirect('/')

    def post(self, request):
        data = {
            'error': None,
        }

        username = request.POST['username']
        password = request.POST['password']

        if not request.user.is_authenticated:
            if username != "" and password != "":
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    data['error'] = "Неправильное имя пользователя или пароль!"

            return render(request, self.template_name, data)
        else:
            return redirect('/')


class SignUpView(View):
    model = User
    template_name = "mainpage/sign_up.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return redirect('/')

    def post(self, request):
        data = {
            'error': None,
        }

        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST["password2"]

        if not request.user.is_authenticated:
            if username != "" and password1 != "":
                if password1 != password2:
                    data['error'] = "Пароли на совпадают!"
                else:
                    User.objects.create_user(username=username, password=password1)
                    user = authenticate(username=username, password=password1)
                    login(request, user)
                    return redirect('/')

            return render(request, self.template_name, data)
        else:
            return redirect('/')


class LinkView(View):
    template_name = "mainpage/error_link.html"

    def get(self, request, short_link):
        try:
            link = Link.objects.get(link2=short_link).link1
            return redirect(link)
        except:
            return render(request, self.template_name)

        # slug = ''.join(random.choice(string.ascii_letters) for x in range(6))


class AccountView(View):
    template_name = "mainpage/account.html"

    def get(self, request):
        if request.user.is_authenticated:

            data = {
                'username': request.user.username,
                'links': Link.objects.all().filter(user=request.user),
                'absolute_url': request.build_absolute_uri()[:-8],
            }

            return render(request, self.template_name, data)
        else:
            return redirect('/')


class CreateLinkView(View):
    template_name = "mainpage/create_link.html"
    template_name_successfully = "mainpage/successfully.html"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return redirect('/')

    def post(self, request):

        data = {
            'error': None,
            'absolute_url': request.build_absolute_uri()[:-12],
        }

        link = request.POST['link']
        if request.user.is_authenticated:
            if validators.url(link):
                try:
                    valid_link1 = Link.objects.get(link1=link)
                    data['error'] = "Такая ссылка уже существует!"
                except:
                    while True:
                        slug = ''.join(random.choice(string.ascii_letters) for x in range(6))
                        try:
                            valid_link2 = Link.objects.get(link2=slug)
                        except:
                            Link.objects.create(user=request.user, link1=link, link2=slug)
                            data['link1'] = link
                            data['link2'] = slug
                            return render(request, self.template_name_successfully, data)
                            break
            else:
                data['error'] = "Ссылка не валидна!"

            return render(request, self.template_name, data)
        else:
            return redirect('/')


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")