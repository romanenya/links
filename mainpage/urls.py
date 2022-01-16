from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view()),
    path('sign_in', views.SignInView.as_view()),
    path('sign_up', views.SignUpView.as_view()),
    path('account', views.AccountView.as_view()),
    path('create_link', views.CreateLinkView.as_view()),
    path('logout', views.LogOutView.as_view()),
    path('<str:short_link>', views.LinkView.as_view()),
]
