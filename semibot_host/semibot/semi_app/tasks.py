from celery import shared_task
import semi_app.helper as helper
from semi_app.models import TaskRequest

@shared_task
def start_matching_task(task_request_id: int):
    record = TaskRequest.objects.filter(id=task_request_id).first()

    if record is None:
        return

    helper.send_matching_server(
        task_datetime=record.task_datetime,
        bachelor_num=record.bachelor_num,
        master_num=record.master_num
    )

    record.delete()