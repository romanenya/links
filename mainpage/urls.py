from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage),
    path('sign_up', views.RegView.as_view()),
]
