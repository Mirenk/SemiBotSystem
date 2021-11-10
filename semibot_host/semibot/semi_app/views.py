from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views import generic
from django.urls import reverse_lazy
from matching.views import JoinView, CancelView
from .forms import LoginForm, MyPasswordChangeForm, TaskRequestForm
from .models import TaskRequest
import semi_app.helper as helper
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from django.utils import timezone
import json


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

    def post(self, request, *args, **kwargs):
        res = super(Join, self).post(request, *args, **kwargs)
        if request.POST.get('btn', '') == 'join':
            self.join_response(self.request.user, self.object)
        else:
            self.decline_response(self.request.user, self.object)

        return res

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
            return self.record_or_send_task(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('semi_app:top'))

    def record_or_send_task(self, form):
        cleaned_data = form.cleaned_data
        # 今すぐ募集開始の場合
        if cleaned_data.get('start_matching_now'):
            helper.send_matching_server(
                task_datetime=cleaned_data.get('task_datetime'),
                bachelor_num=cleaned_data.get('bachelor_num'),
                master_num=cleaned_data.get('master_num'),
                rematching_duration=cleaned_data.get('rematching_duration'),
                matching_end_datetime=cleaned_data.get('matching_end_datetime')
            )
            return redirect(self.success_url)
        else: # 指定時刻に募集開始の場合
            res = super(TaskRequestView, self).form_valid(form)
            # タスク登録
            schedule, create = ClockedSchedule.objects.get_or_create(
                clocked_time=cleaned_data.get('start_matching_datetime')
            )
            PeriodicTask.objects.create(
                clocked=schedule,
                name='全体ゼミ募集_' + timezone.now().strftime('%Y-%m-%d %H:%M'),
                task='semi_app.tasks.start_matching_task',
                args=json.dumps([self.object.id]),
                one_off=True,
            )
            return res

