from django.core.management.base import BaseCommand
from matching.models import TaskRequestRequest, JoinResponseHistory, DeclineResponseHistory, CancelResponseHistory, FillRequireCandidateHistory
import csv

class Command(BaseCommand):
    help = """Generate CSV log"""

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int, required=True)
        parser.add_argument('-o', '--output_path', type=str, default='/var/log/semibot/')

    def __export_join_history_csv(self, filepath: str, queryset):
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['user', 'join_at_date', 'join_at_time'])
            for record in queryset:
                writer.writerow([record.user.username, record.join_at.strftime('%Y/%m/%d'), record.join_at.strftime('%H:%M:%S')])

    def __export_decline_history_csv(self, filepath: str, queryset):
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['user', 'decline_at_date', 'decline_at_time'])
            for record in queryset:
                writer.writerow([record.user.username, record.decline_at.strftime('%Y/%m/%d'), record.decline_at.strftime('%H:%M:%S')])

    def __export_cancel_history_csv(self, filepath: str, queryset):
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['user', 'cancel_at_date', 'cancel_at_time'])
            for record in queryset:
                writer.writerow([record.user.username, record.cancel_at.strftime('%Y/%m/%d'), record.cancel_at.strftime('%H:%M:%S')])

    def __export_fill_require_history_csv(self, filepath, queryset):
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['fill_at_date', 'fill_at_time'])
            for record in queryset:
                writer.writerow([record.join_at.strftime('%Y/%m/%d'), record.join_at.strftime('%H:%M:%S')])

    def handle(self, *args, **options):
        base_path = options['output_path']
        try:
            task_request = TaskRequestRequest.objects.get(id=options['id'])
        except TaskRequestRequest.DoesNotExist:
            print('Not found TaskRequest ID', options['id'])

        self.__export_join_history_csv(base_path + task_request.name + '_join.csv',
                                       JoinResponseHistory.objects.filter(task_request=task_request))
        self.__export_decline_history_csv(base_path + task_request.name + '_decline.csv',
                                          DeclineResponseHistory.objects.filter(task_request=task_request))
        self.__export_cancel_history_csv(base_path + task_request.name + '_cancel.csv',
                                         CancelResponseHistory.objects.filter(task_request=task_request))
        self.__export_fill_require_history_csv(base_path + task_request.name + '_fill.csv',
                                               FillRequireCandidateHistory.objects.filter(task_request=task_request))


