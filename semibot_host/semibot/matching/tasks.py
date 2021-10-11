# 非同期処理用モジュール
# Celeryのセットアップが必要
# 詳しくは https://docs.celeryproject.org/en/master/django/first-steps-with-django.html
from celery import shared_task

from .models import TaskRequestRequest
import matching.matching as matching
import matching.grpc_client as client
from django_celery_beat.models import ClockedSchedule, PeriodicTask

# 人数確認関数
# 同時刻に複数のタスクの終了時刻が来る可能性があるので、ここを並列処理する
@shared_task
def check_joined_candidates(task_request_id: int):
    task_request = TaskRequestRequest.objects.get(id=task_request_id)
    personal_data = client.get_personal_data_dict()
    joined_candidates = task_request.joined_candidates.all().count()

    # 次の人数確認時間に更新
    schedule, create = ClockedSchedule.objects.get_or_create(
        clocked_time=task_request.next_rematching + task_request.rematching_duration
    )
    PeriodicTask.objects.filter(name=task_request.name).update(clocked=schedule)

    # 必要人数に足りていない場合、再募集
    if task_request.require_candidates > joined_candidates:
        print('check_joined_candidates: Start rematching "',task_request.name,'"')
        task = client.get_task_from_name(task_request.task)
        task_request_history = client.get_task_request_histories(task)
        matching.select_candidate_group(task_request, personal_data, task_request_history)
        return

# 終了関数
# TODO:募集終了でも足りなかった場合の検討
@shared_task
def end_matching_task(task_request_id: int):
    task_request = TaskRequestRequest.objects.get(id=task_request_id)

    # 書き込み
    # TODO: 人数が多かった場合、workerを優先度が高い(送付が速かった順)にする
    print("check_time: End ",task_request.name,"'s matching")
    client.record_task_request_history(task_request)
    matching.send_message(task_request=task_request)

    # タスクを削除
    PeriodicTask.objects.filter(name='end_' + task_request.name).delete()
