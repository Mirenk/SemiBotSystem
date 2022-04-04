from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from matching.models import TaskRequestRequest, JoinResponseHistory, DeclineResponseHistory, CancelResponseHistory
from matching.tasks import join_task, cancel_task

class BaseJoinView(LoginRequiredMixin, DetailView):
    model = TaskRequestRequest
    template_name_suffix = '_task_join'
    success_url = reverse_lazy('join_success')
    context_object_name = 'task_request'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        # 依頼送付に居るか調べる
        candidate = obj.requesting_candidates.filter(personal_data=self.request.user).first()
        declined = obj.decline_candidates.filter(personal_data=self.request.user).first()
        if candidate is None and declined is None:
            raise Http404()

        return obj

    def join_response(self, user, task_request):
        JoinResponseHistory.objects.create(user=user, task_request=task_request)
        join_task.delay(task_request_pk=task_request.pk, user_pk=user.pk)

    def decline_response(self, user, task_request):
        DeclineResponseHistory.objects.create(user=user, task_request=task_request)
        cancel_task.delay(task_request_pk=task_request.pk, user_pk=user.pk)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(str(self.success_url))


class BaseCancelView(LoginRequiredMixin, DetailView):
    model = TaskRequestRequest
    template_name_suffix = '_task_cancel'
    success_url = reverse_lazy('cancel_success')
    context_object_name = 'task_request'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        # 依頼送付に居るか調べる
        candidate = obj.joined_candidates.filter(personal_data=self.request.user).first()
        if candidate is None:
            raise Http404()

        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        CancelResponseHistory.objects.create(task_request=self.object, user=self.request.user)
        cancel_task.delay(task_request_pk=self.object.pk, user_pk=self.request.user.pk)
        return HttpResponseRedirect(str(self.success_url))

class Top(TemplateView):
    template_name = 'matching/top.html'

class Join(BaseJoinView):
    """参加者受付"""
    success_url = reverse_lazy('matching:complete')
    template_name = 'matching/task_join.html'

    def post(self, request, *args, **kwargs):
        res = super(Join, self).post(request, *args, **kwargs)
        if request.POST.get('btn', '') == 'join':
            self.join_response(self.request.user, self.object)
        else:
            self.decline_response(self.request.user, self.object)

        return res

class Cancel(BaseCancelView):
    """参加者キャンセル"""
    success_url = reverse_lazy('matching:comlete')
    template_name = 'matching/task_cancel.html'