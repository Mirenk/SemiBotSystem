# 非同期処理用モジュール
# Celeryのセットアップが必要
# 詳しくは https://docs.celeryproject.org/en/master/django/first-steps-with-django.html
from celery import shared_task

from .models import TaskRequestRequest, FillRequireCandidateHistory, LabelValue
import matching.matching as matching
import matching.grpc_client as grpc_client
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from datetime import datetime, timedelta
import json
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

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
        matching.send_request_to_candidates(task_request, personal_data_id_list, is_rematching=True)

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

# 参加受付処理
def join_task(task_request_pk, user_pk):
    task_request = TaskRequestRequest.objects.get(pk=task_request_pk)
    user = get_user_model().objects.get(pk=user_pk)

    # task_requestがis_completeではない場合のみ動作
    if task_request.is_complete:
        return False

    # 処理候補者抽出
    # requestingだった場合、一度declineに下げてから処理
    requesting = task_request.requesting_candidates.filter(personal_data=user).first()
    if requesting:
        with transaction.atomic():
            task_request.requesting_candidates.remove(requesting)
            task_request.decline_candidates.add(requesting)

    candidate = task_request.decline_candidates.filter(personal_data=user).first()
    candidate_data = grpc_client.get_personal_data_from_id(user.username)

    # 依頼送付中から外し参加に付ける
    # トランザクション処理を行う
    with transaction.atomic():
        # ラベルセットの数値を減らす
        # TODO: If label_set == None ?
        label_set = task_request.label_set.all().first()
        for label_name in candidate_data.labels.keys():
            label = label_set.var_label.filter(label__is_dynamic=False).filter(label__name=label_name).first()
            print(label)
            if label is not None:
                if label.value == 0:
                    return False

                new_label, c = LabelValue.objects.get_or_create(label=label.label, value=label.value - 1)
                label_set.var_label.remove(label)
                label_set.var_label.add(new_label)

        task_request.decline_candidates.remove(candidate)
        task_request.joined_candidates.add(candidate)
        print('join_task: Joined ', candidate.personal_data.username)

    # 人数チェック
    if matching.check_fill_candidates(task_request):
        FillRequireCandidateHistory.objects.create(task_request=task_request)

    # メッセージ送信
    candidate_pb = grpc_client.get_personal_data_from_id(user.username)
    matching.send_message(candidate_pb.message_addr, task_request.join_complete_message)

    return True

# 参加キャンセル処理
def cancel_task(task_request_pk, user_pk):
    task_request = TaskRequestRequest.objects.get(pk=task_request_pk)
    user = get_user_model().objects.get(pk=user_pk)

    # task_requestがis_completeではない場合のみ動作
    if task_request.is_complete:
        return False

    # キャンセルしてるのにまた不参加押す不届きもの対応
    decline = task_request.decline_candidates.filter(personal_data=user).first()
    if decline:
        return True

    # 処理候補者抽出
    # joinedじゃない場合、一度joinedに上げてから処理開始
    requesting = task_request.requesting_candidates.filter(personal_data=user).first()
    if requesting:
        with transaction.atomic():
            task_request.requesting_candidates.remove(requesting)
            task_request.joined_candidates.add(requesting)

    candidate = task_request.joined_candidates.filter(personal_data=user).first()
    candidate_data = grpc_client.get_personal_data_from_id(user.username)

    # join_taskと逆のことを行う
    with transaction.atomic():
        # ラベルセットの数値を減らす
        label_set = task_request.label_set.all().first()
        for label_name in candidate_data.labels.keys():
            label = label_set.var_label.filter(label__is_dynamic=False).filter(label__name=label_name).first()

            if label is not None:
                new_label, c = LabelValue.objects.get_or_create(label=label.label, value=label.value + 1)
                label_set.var_label.remove(label)
                label_set.var_label.add(new_label)

        task_request.joined_candidates.remove(candidate)
        task_request.decline_candidates.add(candidate)
        print('join_task: Canceled ', candidate.personal_data.username)

    # メッセージ送信
    candidate_pb = grpc_client.get_personal_data_from_id(user.username)
    matching.send_message(candidate_pb.message_addr, task_request.cancel_complete_message)

    return True