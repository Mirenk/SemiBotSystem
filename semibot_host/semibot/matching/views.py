from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from matching.models import TaskRequestRequest, JoinResponseHistory, DeclineResponseHistory
from matching.matching import join_task, cancel_task

class JoinView(LoginRequiredMixin, DetailView):
    model = TaskRequestRequest
    template_name_suffix = '_task_join'
    success_url = reverse_lazy('join_success')
    context_object_name = 'task_request'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        # 依頼送付に居るか調べる
        candidate = obj.requesting_candidates.filter(personal_data=self.request.user).first()
        if candidate is None:
            raise Http404()

        return obj

    def join_response(self, user, task_request):
        JoinResponseHistory.objects.create(user=user, task_request=task_request)
        join_task(task_request, user)

    def decline_response(self, user, task_request):
        DeclineResponseHistory.objects.create(user=user, task_request=task_request)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(str(self.success_url))


class CancelView(LoginRequiredMixin, DetailView):
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
        cancel_task(self.object, self.request.user)
        return HttpResponseRedirect(str(self.success_url))