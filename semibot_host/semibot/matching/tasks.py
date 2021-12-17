# 非同期処理用モジュール
# Celeryのセットアップが必要
# 詳しくは https://docs.celeryproject.org/en/master/django/first-steps-with-django.html
from celery import shared_task

from .models import TaskRequestRequest
import matching.matching as matching
import matching.grpc_client as client
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from datetime import datetime, timedelta
import json
from django.conf import settings

# 人数確認関数
# 同時刻に複数のタスクの終了時刻が来る可能性があるので、ここを並列処理する
@shared_task
def check_joined_candidates(task_request_id: int):
    task_request = TaskRequestRequest.objects.get(id=task_request_id)

    # もし完了したタスクだった場合、すぐに終了
    if task_request.is_complete:
        return

    # 必要人数に足りていない場合、再募集
    if not matching.check_fill_candidates(task_request):
        print('check_joined_candidates: Start rematching "',task_request.name,'"')
        personal_data = matching.prepare_personal_data(task_request)
        personal_data_id_list = matching.select_candidate_group(task_request, personal_data)
        matching.send_request_to_candidates(task_request, personal_data, personal_data_id_list, is_rematching=True)

    # 次の人数確認時間に更新
    next_rematching = task_request.next_rematching + task_request.rematching_duration
    # 土日の再募集をスキップ
    if settings.MATCHING_SKIP_WEEKENDS:
        if next_rematching.weekday() > 4: # 次回が土日だった場合
            next_rematching += timedelta(days=2)

    if next_rematching < task_request.matching_end_datetime:
        schedule, create = ClockedSchedule.objects.get_or_create(
            clocked_time=task_request.next_rematching + task_request.rematching_duration
        )
        check_joined_candidates_task = PeriodicTask.objects.create(
            clocked=schedule,
            name=task_request.name + datetime.now().strftime("%y%m%d%H%M"),
            task='matching.tasks.check_joined_candidates',
            args=json.dumps([task_request_id]),
            one_off=True,
        )
        task_request.check_joined_candidates_task = check_joined_candidates_task
        task_request.next_rematching = next_rematching

# 終了関数
# TODO:募集終了でも足りなかった場合の検討
@shared_task
def end_matching_task(task_request_id: int):
    task_request = TaskRequestRequest.objects.get(id=task_request_id)

    if not task_request.is_complete:
        print("end_mathcing_task: can't match ", task_request.name)
        # 依頼を完了状態にする
        task_request.is_complete = True
        task_request.save()