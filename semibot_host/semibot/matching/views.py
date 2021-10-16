from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from matching.models import TaskRequestRequest

@login_required
class JoinView(DetailView):
    model = TaskRequestRequest
    template_name_suffix = '_task_join'
    success_url = reverse_lazy('join_success')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        # 依頼送付に居るか調べる
        candidate = obj.requesting_candidates.filter(persona_data=self.request.user).first()
        if candidate is None:
            raise Http404()

        return obj

    def post(self, request):
        return HttpResponseRedirect(str(self.success_url))


@login_required
class CancelView(DetailView):
    pass