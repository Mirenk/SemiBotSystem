from .models import *

from .matching_pb import server_pb2, server_pb2_grpc

from django.db import transaction
from datetime import datetime

#
# サービス定義
#
class MatchingServer(server_pb2_grpc.MatchingServerServicer):
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

            # ManyToManyのための一時記録
            task_request.save()

            # ラベル処理
            label_set_pb_list = request.label_set
            for label_set_pb in label_set_pb_list:
                # 空のラベルセットを作成
                label_set = LabelSet.objects.create()

                # 固定ラベル処理
                for label_pb in label_set_pb.const_label:
                    label, create = Label.objects.get_or_create(name=label_pb.name)
                    label_set.const_label.add(label)

                # 数値ラベル処理
                for label_value_pb in label_set_pb.var_label:
                    label, create = Label.objects.get_or_create(name=label_value_pb.label.name)
                    label_value, create = LabelValue.objects.get_or_create(label_id=label.id, value=label_value_pb.value)

                    label_set.var_label.add(label_value)

                task_request.label_set.add(label_set)

        response.result = server_pb2.AddTaskRequestResponse.Result.SUCCESS

        return response

#
# Handler(サービスをサーバに登録するための関数)
#
def grpc_handlers(server):
    server_pb2_grpc.add_MatchingServerServicer_to_server(MatchingServer(), server)