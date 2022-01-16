from django.shortcuts import render, redirect
from django.views import View
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class MainView(View):
    def get(self, request):
        if request.user.is_authenticated:
            pass
        else:
            return redirect('/sign_in')


class SignInView(View):
    template_name = "mainpage/sign_in.html"
    form = UserForm
    model = User

    def get(self, request):
        data = {
            'form': self.form,
        }
        return render(request, self.template_name, data)

    def post(self, request):
        form = self.form(request.POST)
        username = form['username'].value()
        password = form['password'].value()
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    print("Account doesn't active!")
            else:
                print("Invalid username or password")
        data = {
            'form': form,
        }
        return render(request, self.template_name, data)
