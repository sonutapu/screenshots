from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, register, login_user, logout_user
urlpatterns = [
    path('', home, name="home"),
    path("register", register, name="register"),
    path("login_user", login_user, name="login_user"),
    path("logout_user", logout_user, name="logout_user"),

]