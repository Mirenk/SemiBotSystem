from celery import shared_task
import semi_app.helper as helper
from semi_app.models import TaskRequest
from django.utils.timezone import localtime

@shared_task
def start_matching_task(task_request_id: int):
    record = TaskRequest.objects.filter(id=task_request_id).first()

    if record is None:
        return

    helper.send_matching_server(
        task_datetime=localtime(record.task_datetime),
        bachelor_num=record.bachelor_num,
        master_num=record.master_num,
        rematching_duration=record.rematching_duration,
        matching_end_datetime=record.matching_end_datetime,
        is_random=record.is_random
    )

    record.delete()