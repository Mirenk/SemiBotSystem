from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from .forms import LoginForm


class Top(generic.TemplateView):
    template_name = 'semi_app/top.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'semi_app/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'semi_app/top.html'