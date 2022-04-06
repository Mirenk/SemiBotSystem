from .forms import LoginForm
from django.contrib.auth.views import LoginView, LogoutView

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'custom_auth/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'matching/top.html'
