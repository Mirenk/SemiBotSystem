from django.core.management.base import BaseCommand
from django.utils.timezone import localtime
from matching.models import TaskRequestRequest, JoinResponseHistory, DeclineResponseHistory, CancelResponseHistory, FillRequireCandidateHistory
import csv
import os

class Command(BaseCommand):
    help = """Generate CSV log"""

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int, default=0)
        parser.add_argument('-o', '--output_path', type=str, default='/var/log/semibot/')

    def __export_join_history_csv(self, filepath: str, queryset):
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['user', 'join_at_date', 'join_at_time'])
            for record in queryset:
                dt = localtime(record.join_at)
                writer.writerow([record.user.username, dt.strftime('%Y/%m/%d'), dt.strftime('%H:%M:%S')])

    def __export_decline_history_csv(self, filepath: str, queryset):
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['user', 'decline_at_date', 'decline_at_time'])
            for record in queryset:
                dt = localtime(record.decline_at)
                writer.writerow([record.user.username, dt.strftime('%Y/%m/%d'), dt.strftime('%H:%M:%S')])

    def __export_cancel_history_csv(self, filepath: str, queryset):
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['user', 'cancel_at_date', 'cancel_at_time'])
            for record in queryset:
                dt = localtime(record.cancel_at)
                writer.writerow([record.user.username, dt.strftime('%Y/%m/%d'), dt.strftime('%H:%M:%S')])

    def __export_fill_require_history_csv(self, filepath, queryset):
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['fill_at_date', 'fill_at_time'])
            for record in queryset:
                dt = localtime(record.fill_at)
                writer.writerow([dt.strftime('%Y/%m/%d'), dt.strftime('%H:%M:%S')])

    def __export_all_csv(self, base_path, task_request):
        target_path = base_path + task_request.name
        os.makedirs(target_path, exist_ok=True)

        self.__export_join_history_csv(target_path + '/join.csv',
                                       JoinResponseHistory.objects.filter(task_request=task_request))
        self.__export_decline_history_csv(target_path + '/decline.csv',
                                          DeclineResponseHistory.objects.filter(task_request=task_request))
        self.__export_cancel_history_csv(target_path + '/cancel.csv',
                                         CancelResponseHistory.objects.filter(task_request=task_request))
        self.__export_fill_require_history_csv(target_path + '/fill.csv',
                                               FillRequireCandidateHistory.objects.filter(task_request=task_request))

    def handle(self, *args, **options):
        base_path = options['output_path']

        if id > 0:
            try:
                task_request = TaskRequestRequest.objects.get(id=options['id'])
            except TaskRequestRequest.DoesNotExist:
                print('Not found TaskRequest ID', options['id'])
                return
            self.__export_all_csv(base_path, task_request)
        elif id == 0:
            for task_request in TaskRequestRequest.objects.all():
                self.__export_all_csv(base_path, task_request)
