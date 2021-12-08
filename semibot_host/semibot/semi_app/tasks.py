from celery import shared_task
import semi_app.helper as helper
from semi_app.models import TaskRequest
from django.utils import timezone
from django.utils.timezone import localtime
import random
from datetime import datetime, time, timedelta

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

@shared_task
def set_random_semi():
    now = localtime(timezone.now())
    while True:
        semi_dt1 = choice_random_semi_date(now)
        semi_dt2 = choice_random_semi_date(now)

        if semi_dt1 != semi_dt2:
            break

    print(semi_dt1)
    print(semi_dt2)

# TODO: 一週間期間を開けるようにする
def choice_random_semi_date(dt: datetime):
    if dt.weekday() != 0:
        raise ValueError("datetime is not Monday")

    weekday = random.randint(0, 4) # 曜日をランダム決定(月曜が0)
    start_time = [time(hour=9), time(hour=13), time(hour=14, minute=30)]
    start_time_index = random.randint(0,2) # 時間をランダム決定(1~2限:0, 3~4限:1, 4~5限:2)

    # 全体ゼミと同じだった場合、振り直し
    if weekday == 4 and start_time_index == 0:
        print("re")
        return choice_random_semi_date(dt)

    day = dt.day + weekday
    return dt.replace(day=day, hour=start_time[start_time_index].hour, minute=start_time[start_time_index].minute, second=0, microsecond=0)