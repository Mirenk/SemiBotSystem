from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.views import generic
from django.urls import reverse_lazy
from matching.views import JoinView, CancelView
from .forms import LoginForm, MyPasswordChangeForm


class Top(generic.TemplateView):
    template_name = 'semi_app/top.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'semi_app/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'semi_app/top.html'


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('semi_app:password_change_done')
    template_name = 'semi_app/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'semi_app/password_change_done.html'

class Join(JoinView):
    """参加者受付"""
    success_url = reverse_lazy('semi_app:top')
    template_name = 'semi_app/semi_task_join.html'

class Cancel(CancelView):
    """参加者キャンセル"""
    success_url = reverse_lazy('semi_app:top')
    template_name = 'semi_app/semi_task_cancel.html'
