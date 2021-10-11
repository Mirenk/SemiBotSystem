# 非同期処理用モジュール
# Celeryのセットアップが必要
# 詳しくは https://docs.celeryproject.org/en/master/django/first-steps-with-django.html
from celery import shared_task

from .models import TaskRequestRequest
from matching_pb import type_pb2
import matching.matching as matching
import matching.grpc_client as client
from datetime import datetime
from django.utils.timezone import localtime

# 人数確認関数
# 同時刻に複数のタスクの終了時刻が来る可能性があるので、ここを並列処理する
@shared_task
def check_joined_candidates(task_request_id: int):
    task_request = TaskRequestRequest.objects.get(id=task_request_id)
    personal_data = client.get_personal_data_dict()
    joined_candidates = task_request.joined_candidates.all().count()

    # 必要人数に足りていない場合、再募集
    if task_request.require_candidates > joined_candidates:
        print('check_joined_candidates: Start rematching "',task_request.name,'"')
        task = client.get_task_from_name(task_request.task)
        task_request_history = client.get_task_request_histories(task)
        matching.select_candidate_group(task_request, personal_data, task_request_history)
        return


# 時刻確認関数
# プロジェクトに定期実行登録が必要、詳しくは　https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
# もし再募集時間であったら人数確認を行う
# 募集終了時間であったらクライアント側に通知を行い、募集終了
@shared_task
def check_time():
    # 時刻取得
    now = datetime.now()

    # 終了の募集依頼を抽出
    end_tasks = TaskRequestRequest.objects.filter(matching_end_datetime__lte=now)

    if end_tasks is not None:
        for end_task in end_tasks:
            # 書き込みなので並列化せず一件ずつ処理
            # TODO: 人数が多かった場合、workerを優先度が高い(送付が速かった順)にする
            print("check_time: End ",end_task.name,"'s matching")
            client.record_task_request_history(end_task)
            matching.send_message(task_request=end_task)

    # 再募集期間の募集依頼を抽出
    rematching_tasks = TaskRequestRequest.objects.filter(next_rematching__lte=now)

    if rematching_tasks is not None:
        for rematching_task in rematching_tasks:
            # 再募集期間の2倍以上ある場合はそのまま現在の再募集時間+期間
            # ない場合は終了時刻と同じにする(Viewsの方でここが同じだった場合にキャンセル不可とするため)
            next_rematching = rematching_task.next_rematching + rematching_task.rematching_duration
            if next_rematching + rematching_task.rematching_duration >= rematching_task.matching_end_datetime:
                rematching_task.next_rematching = rematching_task.matching_end_datetime
            else:
                rematching_task.next_rematching = next_rematching
            rematching_task.save()
            print(rematching_task.next_rematching)
            print('check_time: Next ',rematching_task.name,"'s rematching date is ",localtime(rematching_task.next_rematching).strftime('%Y-%m-%d %H:%M'))

            # 人数確認を呼ぶ(非同期)
            check_joined_candidates.delay(rematching_task.id)