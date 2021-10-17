from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from matching.models import TaskRequestRequest
from matching.matching import join_task, cancel_task

class JoinView(DetailView, LoginRequiredMixin):
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        join_task(self.object, self.request.user)
        return HttpResponseRedirect(str(self.success_url))


class CancelView(DetailView, LoginRequiredMixin):
    pass