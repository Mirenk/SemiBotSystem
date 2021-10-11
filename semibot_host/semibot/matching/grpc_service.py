import inspect

import json

from .models import *

from matching_pb import server_pb2, server_pb2_grpc
from .dynamic_label import DynamicLabel

from django.db import transaction
from datetime import datetime

from django_celery_beat.models import ClockedSchedule, PeriodicTask

#
# サービス定義
#
class MatchingServer(server_pb2_grpc.MatchingServerServicer):
    @classmethod
    def __get_label_model_from_label_pb(cls, label_pb):
        # dynamic_labelからメソッドを取得
        methods = [x[0] for x in inspect.getmembers(DynamicLabel(), inspect.ismethod)]

        if label_pb.name in methods:
            # 動的ラベルの場合、フラグを立てる
            label, create = Label.objects.get_or_create(name=label_pb.name, is_dynamic=True)
        else:
            # 普通のラベルの場合
            label, create = Label.objects.get_or_create(name=label_pb.name)

        return label

    def AddTaskRequest(self, request, context):
        response = server_pb2.AddTaskRequestResponse()

        with transaction.atomic():
            # 記録用オブジェクト作成
            task_request = TaskRequestRequest()
            task_request.name = request.task_request.name
            task_request.task = request.task_request.task.name
            task_request.task_datetime = datetime.fromtimestamp(request.task_request.task_date.seconds)
            task_request.matching_end_datetime = datetime.fromtimestamp(request.matching_end_date.seconds)
            task_request.callback_url = request.callback_url
            task_request.require_candidates = request.require_candidates
            task_request.max_candidates = request.max_candidates

            td = request.rematching_duration.ToTimedelta()
            task_request.rematching_duration = td
            task_request.next_rematching = datetime.now() + td

            # ManyToManyのための一時記録
            task_request.save()

            # ラベル処理
            label_set_pb_list = request.label_set
            for label_set_pb in label_set_pb_list:
                # 空のラベルセットを作成
                label_set = LabelSet.objects.create()

                # 固定ラベル処理
                for label_pb in label_set_pb.const_label:
                    label = self.__get_label_model_from_label_pb(label_pb)
                    label_set.const_label.add(label)

                # 数値ラベル処理
                for label_value_pb in label_set_pb.var_label:
                    label = self.__get_label_model_from_label_pb(label_value_pb.label)
                    label_value, create = LabelValue.objects.get_or_create(label_id=label.id, value=label_value_pb.value)

                    label_set.var_label.add(label_value)

                task_request.label_set.add(label_set)

        response.result = server_pb2.AddTaskRequestResponse.Result.SUCCESS

        # 人数チェックのタスク登録
        schedule, create = ClockedSchedule.objects.get_or_create(
            clocked_time=task_request.next_rematching
        )
        PeriodicTask.objects.create(
            clocked=schedule,
            name=task_request.name,
            task='matching.tasks.check_joined_candidates',
            args=json.dumps([task_request.id]),
            one_off=True,
        )

        return response

#
# Handler(サービスをサーバに登録するための関数)
#
def grpc_handlers(server):
    server_pb2_grpc.add_MatchingServerServicer_to_server(MatchingServer(), server)