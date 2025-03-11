from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name = "register"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("list/", views.list_instances, name = "list_instances"),
    path("view/", views.view, name = "view"),
    path("average/", views.average, name = "average"),
    path("rate/", views.rate, name = "rate")
]
