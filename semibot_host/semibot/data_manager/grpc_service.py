from .models import *
from django.db import transaction

from .matching_pb import data_manage_pb2, data_manage_pb2_grpc, type_pb2
from google.protobuf import timestamp_pb2

from datetime import datetime

#
# サービス定義
#
class DataManage(data_manage_pb2_grpc.DataManageServicer):
    ##################################################
    ## クラスメソッド(DjangoのModel -> Protobufの変換等) ##
    ##################################################
    # ラベルのqueryset -> ProtobufのLabelリスト
    @classmethod
    def __get_label_pb_list_from_label_queryset(cls, labels):
        labels_pb = []

        for label in labels:
            label_pb = type_pb2.Label(name=label.name)
            labels_pb.append(label_pb)

        return labels_pb

    # 値付きラベルのqueryset -> ProtobufのLabelValueリスト
    @classmethod
    def __get_labelvalue_pb_list_from_labelvalue_queryset(cls, label_values):
        label_values_pb = []

        for label_value in label_values:
            label_pb = type_pb2.Label(name=label_value.label.name)
            label_value_pb = type_pb2.LabelValue(label=label_pb, value=label_value.value)
            label_values_pb.append(label_value_pb)

        return label_values_pb

    # タスク -> ProtobufのTask
    @classmethod
    def __get_task_pb_from_task_record(cls, task):
        # タスク作成
        task_pb = type_pb2.Task()
        task_pb.name = task.name

        # ProtobufのLabelリストを生成
        label_list = cls.__get_label_pb_list_from_label_queryset(task.require_label.all())
        # ProtobufのLabelValueリストを生成
        label_value_list = cls.__get_labelvalue_pb_list_from_labelvalue_queryset(task.require_label_value.all())

        # 各ラベル登録
        task_pb.require_label.extend(label_list)
        task_pb.require_label_value.extend(label_value_list)

        return task_pb

    # 個人情報モデル -> ProtobufのPersonalData
    @classmethod
    def __get_personaldata_pb_from_personaldata_record(cls, personal_data):
        # ラベル以外のPersonalDataを先に作成
        personal_data_pb = type_pb2.PersonalData()
        personal_data_pb.id = personal_data.username
        personal_data_pb.name = personal_data.first_name + personal_data.last_name
        personal_data_pb.message_addr = personal_data.message_addr

        # ProtobufのLabelリストを生成
        label_list = cls.__get_label_pb_list_from_label_queryset(personal_data.label.all())

        # ラベルを登録
        personal_data_pb.labels.extend(label_list)

        return personal_data_pb

    # 個人情報のqueryset -> ProtobufのPersonalDataリスト
    @classmethod
    def __get_personaldata_list_from_personaldata_queryset(cls, personal_data_list):
        personal_data_pb_list = []

        for personal_data in personal_data_list:
            personal_data_pb = cls.__get_personaldata_pb_from_personaldata_record(personal_data)

            personal_data_pb_list.append(personal_data_pb)

        return personal_data_pb_list

    #########################
    ## Protobufのメソッド実装 ##
    #########################
    def ListLabels(self, request, context):
        response = data_manage_pb2.ListLabelsResponse()
        labels_pb = self.__get_label_pb_list_from_label_queryset(Label.objects.all())

        response.labels.extend(labels_pb)

        return response

    def ListPersonalData(self, request, context):
        response = data_manage_pb2.ListPersonalDataResponse()
        personal_data_list = PersonalData.objects.all()

        # responseに追加
        response.personal_data.extend(self.__get_personaldata_list_from_personaldata_queryset(personal_data_list))

        return response

    def ListTasks(self, request, context):
        response = data_manage_pb2.ListTasksResponse()
        task_list = Task.objects.all()

        for task in task_list:
            task_pb = self.__get_task_pb_from_task_record(task)

            # responseに追加
            response.tasks.append(task_pb)

        return response

    def GetTaskFromName(self, request, context):
        task_name = request.name
        task = Task.objects.filter(name=task_name).first()

        return self.__get_task_pb_from_task_record(task)

    def GetTaskRequestHistories(self, request, context):
        response = data_manage_pb2.GetTaskRequestHistoriesResponse()

        # タスク取得
        task_name = request.name
        task = Task.objects.filter(name=task_name).first()
        # 後でつけるため、変換しておく
        task_pb = self.__get_task_pb_from_task_record(task)

        # 依頼取得
        task_requests = TaskRequest.objects.filter(task=task)

        for task_request in task_requests:
            task_request_pb = type_pb2.TaskRequestData()

            # 依頼名
            task_request_pb.name = task_request.name
            # タスク
            task_request_pb.task.CopyFrom(task_pb)
            # 時刻
            task_request_pb.task_date.CopyFrom(timestamp_pb2.Timestamp(seconds=int(task_request.work_datetime.timestamp())))
            # 参加者
            worker_pb_list = self.__get_personaldata_list_from_personaldata_queryset(task_request.worker.all())
            task_request_pb.worker.extend(worker_pb_list)
            # 固定ラベル
            recommend_label_pb_list = self.__get_label_pb_list_from_label_queryset(task_request.recommend_label.all())
            task_request_pb.recommend_label.extend(recommend_label_pb_list)
            # 数値ラベル
            recommend_label_value_pb_list = self.__get_labelvalue_pb_list_from_labelvalue_queryset(task_request.recommend_label_value.all())
            task_request_pb.recommend_label_value.extend(recommend_label_value_pb_list)

            # responseに追加
            response.task_requests.append(task_request_pb)

        return response

    def GetPersonalDataFromId(self, request, context):
        personal_data = PersonalData.objects.filter(username=request.id).first()
        personal_data_pb = self.__get_personaldata_pb_from_personaldata_record(personal_data)

        return personal_data_pb

    def RecordTaskRequestHistory(self, request, context):
        response = data_manage_pb2.RecordTaskRequestHistoryResult()

        with transaction.atomic():
            # 記録用オブジェクト作成
            task_request = TaskRequest()
            task_request.name = request.name
            task_request.work_datetime = datetime.fromtimestamp(request.task_date.seconds)

            # タスク処理
            task = Task.objects.filter(name=request.task.name).first()
            if task is None:
                response.result = data_manage_pb2.RecordTaskRequestHistoryResult.Result.FAILED
                response.message = 'Not found task: ' + request.task.name
                del task_request
                return response
            task_request.task = task

            # ManyToManyのための一時記録
            task_request.save()

            # 参加者処理
            worker_pb = request.worker
            for personal_data_pb in worker_pb:
                personal_data = PersonalData.objects.filter(username=personal_data_pb.id).first()

                if personal_data is None:
                    response.result = data_manage_pb2.RecordTaskRequestHistoryResult.Result.FAILED
                    response.message = 'Not found personal_data: ' + personal_data_pb.name
                    del task_request
                    return response

                task_request.worker.add(personal_data)

            # 固定ラベル処理
            labels_pb = request.recommend_label
            for label_pb in labels_pb:
                label = Label.objects.filter(name=label_pb.name).first()

                if label is None:
                    response.result = data_manage_pb2.RecordTaskRequestHistoryResult.Result.FAILED
                    response.message = 'Not found label: ' + label_pb.name
                    del task_request
                    return response

                task_request.recommend_label.add(label)

            # 数値ラベル処理
            label_values_pb = request.recommend_label_value
            for label_value_pb in label_values_pb:
                label = Label.objects.filter(name=label_value_pb.label.name).first()
                if label is None:
                    response.result = data_manage_pb2.RecordTaskRequestHistoryResult.Result.FAILED
                    response.message = 'Not found label: ' + label_pb.name
                    del task_request
                    return response

                label_value, create = LabelValue.objects.get_or_create(label_id=label.id, value=label_value_pb.value)

                task_request.recommend_label_value.add(label_value)

        response.result = data_manage_pb2.RecordTaskRequestHistoryResult.Result.SUCCESS
        return response

#
# Handler(サービスをサーバに登録するための関数)
#
def grpc_handlers(server):
    data_manage_pb2_grpc.add_DataManageServicer_to_server(DataManage(), server)
