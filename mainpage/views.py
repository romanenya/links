from django.shortcuts import render, redirect
from django.views import View

def mainpage(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/sign_up')

class RegView(View):
    template_name = "mainpage/index.html"

    def get(self, request):
        return render(request, self.template_name)
