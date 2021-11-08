# 非同期処理用モジュール
# Celeryのセットアップが必要
# 詳しくは https://docs.celeryproject.org/en/master/django/first-steps-with-django.html
from celery import shared_task

from .models import TaskRequestRequest
import matching.matching as matching
import matching.grpc_client as client
from django_celery_beat.models import ClockedSchedule

# 人数確認関数
# 同時刻に複数のタスクの終了時刻が来る可能性があるので、ここを並列処理する
@shared_task
def check_joined_candidates(task_request_id: int):
    task_request = TaskRequestRequest.objects.get(id=task_request_id)
    personal_data = client.get_personal_data_dict()
    joined_candidates = task_request.joined_candidates.all().count()

    # 次の人数確認時間に更新
    if task_request.check_joined_candidates_task is not None:
        schedule, create = ClockedSchedule.objects.get_or_create(
            clocked_time=task_request.next_rematching + task_request.rematching_duration
        )
        task_request.check_joined_candidates_task.clocked = schedule
        task_request.check_joined_candidates_task.enabled = True

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
    # 候補者取得
    # この時、依頼送付が古い人順に並べる
    candidates = task_request.joined_candidates.all().order_by('request_datetime')

    # 候補者が多かった場合、削除
    if candidates.count() > task_request.max_candidates:
        for remove_candidate in candidates[task_request.max_candidates:]:
            task_request.joined_candidates.remove(remove_candidate)

    # 書き込み
    print("check_time: End ",task_request.name,"'s matching")
    client.record_task_request_history(task_request)
    matching.send_result_message(task_request=task_request)

    # 依頼を削除
    task_request.delete()

    # タスクを削除
    try:
        task_request.end_matching_task.delete()
        task_request.check_joined_candidates_task.delete()
    except AttributeError:
        pass
