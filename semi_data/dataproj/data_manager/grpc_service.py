from .models import *
from django.db import transaction, close_old_connections
from django.contrib.auth import get_user_model

from matching_pb import data_manage_pb2, data_manage_pb2_grpc, type_pb2
from google.protobuf import timestamp_pb2

from datetime import datetime, timezone

# ユーザモデル定義
# これでどのような認証を使っても動作が変わらない
User = get_user_model()

#
# サービス定義
#
class DataManage(data_manage_pb2_grpc.DataManageServicer):
    ##################################################
    ## クラスメソッド(DjangoのModel -> Protobufの変換等) ##
    ##################################################
    # ラベルのqueryset -> ProtobufのLabel辞書登録
    @classmethod
    def __set_label_pb_dict_from_label_queryset(cls, labels, labels_pb):
        for label in labels:
            label_pb = type_pb2.Label(name=label.name)
            labels_pb[label.name].CopyFrom(label_pb)

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

        # ProtobufのLabel辞書を生成
        cls.__set_label_pb_dict_from_label_queryset(task.require_label.all(), task_pb.require_label)
        # ProtobufのLabelValueリストを生成
        label_value_list = cls.__get_labelvalue_pb_list_from_labelvalue_queryset(task.require_label_value.all())

        # 各ラベル登録
        task_pb.require_label_value.extend(label_value_list)

        return task_pb

    # 個人情報モデル -> ProtobufのPersonalData
    @classmethod
    def __get_personaldata_pb_from_personaldata_record(cls, personal_data):
        # ラベル以外のPersonalDataを先に作成
        personal_data_pb = type_pb2.PersonalData()
        personal_data_pb.id = personal_data.username
        personal_data_pb.name = personal_data.last_name + personal_data.first_name

        # message_addr作成
        message_addr = personal_data.message_addr.filter(is_primary=True).first()
        if message_addr is not None:
            message_addr_pb = type_pb2.MessageAddress()
            message_addr_pb.userid = message_addr.userid
            message_addr_pb.method = message_addr.method

            personal_data_pb.message_addr.CopyFrom(message_addr_pb)

        # Label辞書を登録
        cls.__set_label_pb_dict_from_label_queryset(personal_data.label.all(), personal_data_pb.labels)

        return personal_data_pb

    # 個人情報のqueryset -> ProtobufのPersonalData辞書登録
    @classmethod
    def __set_personaldata_dict_from_personaldata_queryset(cls, personal_data_list, personal_data_dict):

        for personal_data in personal_data_list:
            personal_data_pb = cls.__get_personaldata_pb_from_personaldata_record(personal_data)

            personal_data_dict[personal_data.username].CopyFrom(personal_data_pb)

    #########################
    ## Protobufのメソッド実装 ##
    #########################
    def ListLabels(self, request, context):
        response = data_manage_pb2.ListLabelsResponse()
        close_old_connections()
        self.__set_label_pb_dict_from_label_queryset(Label.objects.all(), response.labels)

        return response

    def ListPersonalData(self, request, context):
        response = data_manage_pb2.ListPersonalDataResponse()
        close_old_connections()
        personal_data_list = PersonalData.objects.all()

        # responseに追加
        self.__set_personaldata_dict_from_personaldata_queryset(personal_data_list, response.personal_data)

        return response

    def ListTasks(self, request, context):
        response = data_manage_pb2.ListTasksResponse()
        close_old_connections()
        task_list = Task.objects.all()

        for task in task_list:
            task_pb = self.__get_task_pb_from_task_record(task)

            # responseに追加
            response.tasks.append(task_pb)

        return response

    def GetTaskFromName(self, request, context):
        task_name = request.name
        close_old_connections()
        task = Task.objects.filter(name=task_name).first()

        return self.__get_task_pb_from_task_record(task)

    def GetTaskRequestHistories(self, request, context):
        response = data_manage_pb2.GetTaskRequestHistoriesResponse()

        # タスク取得
        # TODO: Noneが来た場合…
        task_name = request.name
        close_old_connections()
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
            self.__set_personaldata_dict_from_personaldata_queryset(task_request.worker.all(), task_request_pb.worker)
            # 固定ラベル
            self.__set_label_pb_dict_from_label_queryset(task_request.recommend_label.all(), task_request_pb.recommend_label)
            # 数値ラベル
            recommend_label_value_pb_list = self.__get_labelvalue_pb_list_from_labelvalue_queryset(task_request.recommend_label_value.all())
            task_request_pb.recommend_label_value.extend(recommend_label_value_pb_list)

            # responseに追加
            response.task_requests.append(task_request_pb)

        return response

    def GetPersonalDataFromId(self, request, context):
        close_old_connections()
        personal_data = PersonalData.objects.filter(username=request.id).first()
        personal_data_pb = self.__get_personaldata_pb_from_personaldata_record(personal_data)

        return personal_data_pb

    def RecordTaskRequestHistory(self, request, context):
        response = data_manage_pb2.RecordTaskRequestHistoryResult()

        close_old_connections()
        with transaction.atomic():
            # 記録用オブジェクト作成
            task_request = TaskRequest()
            task_request.name = request.name
            task_request.work_datetime = datetime.fromtimestamp(request.task_date.seconds, timezone.utc)

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
            for username in worker_pb.keys():
                personal_data = PersonalData.objects.filter(username=username).first()

                if personal_data is None:
                    response.result = data_manage_pb2.RecordTaskRequestHistoryResult.Result.FAILED
                    response.message = 'Not found personal_data: ' + username
                    del task_request
                    return response

                task_request.worker.add(personal_data)

            # 固定ラベル処理
            labels_pb = request.recommend_label
            for label_name in labels_pb.keys():
                label = Label.objects.filter(name=label_name).first()

                if label is None:
                    response.result = data_manage_pb2.RecordTaskRequestHistoryResult.Result.FAILED
                    response.message = 'Not found label: ' + label_name
                    del task_request
                    return response

                task_request.recommend_label.add(label)

            # 数値ラベル処理
            label_values_pb = request.recommend_label_value
            for label_value_pb in label_values_pb:
                label = Label.objects.filter(name=label_value_pb.label.name).first()
                if label is None:
                    response.result = data_manage_pb2.RecordTaskRequestHistoryResult.Result.FAILED
                    response.message = 'Not found label: ' + labels_pb.name
                    del task_request
                    return response

                label_value, create = LabelValue.objects.get_or_create(label_id=label.id, value=label_value_pb.value)

                task_request.recommend_label_value.add(label_value)

        response.result = data_manage_pb2.RecordTaskRequestHistoryResult.Result.SUCCESS
        return response

    def Auth(self, request, context):
        responce = data_manage_pb2.AuthResult()

        username = request.username
        password = request.password

        result = User.objects.filter(username=username).filter(password=password)

        if result is not None:
            responce.result = True
        else:
            responce.result = False

        return responce

#
# Handler(サービスをサーバに登録するための関数)
#
def grpc_handlers(server):
    data_manage_pb2_grpc.add_DataManageServicer_to_server(DataManage(), server)
