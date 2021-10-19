from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views import generic
from django.urls import reverse_lazy
from matching.views import JoinView, CancelView
from .forms import LoginForm, MyPasswordChangeForm, TaskRequestForm
from .models import TaskRequest


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

class TaskRequestView(CreateView, LoginRequiredMixin):
    """依頼受付"""
    form_class = TaskRequestForm
    model = TaskRequest
    template_name = 'semi_app/task_request_create.html'
    success_url = reverse_lazy('semi_app:top')

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'semi_app/task_request_confirm.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'semi_app/task_request_create.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('semi_app:top'))

