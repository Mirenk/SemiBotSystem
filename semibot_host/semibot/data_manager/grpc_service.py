from .models import *

from .matching_pb import data_manage_pb2, data_manage_pb2_grpc, type_pb2

# サービス定義
class DataManage(data_manage_pb2_grpc.DataManageServicer):
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

    def ListLabels(self, request, context):
        response = data_manage_pb2.ListLabelsResponse()
        labels_pb = self.__get_label_pb_list_from_label_queryset(Label.objects.all())

        response.labels.extend(labels_pb)

        return response

    def ListPersonalData(self, request, context):
        response = data_manage_pb2.ListPersonalDataResponse()
        personal_data_list = PersonalData.objects.all()

        for personal_data in personal_data_list:
            # ラベル以外のPersonalDataを先に作成
            personal_data_pb = type_pb2.PersonalData()
            personal_data_pb.id = personal_data.username
            personal_data_pb.name = personal_data.first_name + personal_data.last_name
            personal_data_pb.message_addr = personal_data.message_addr

            # ProtobufのLabelリストを生成
            label_list = self.__get_label_pb_list_from_label_queryset(personal_data.label.all())

            # ラベルを登録
            personal_data_pb.labels.extend(label_list)

            # responseに追加
            response.personal_data.append(personal_data_pb)

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
        pass

    def GetTaskRequestHistories(self, request, context):
        pass

    def GetPersonalDataFromId(self, request, context):
        pass

    def RecordTaskRequestHistory(self, request, context):
        pass

# Handler
def grpc_hadlers(server):
    data_manage_pb2_grpc.add_DataManageServicer_to_server(DataManage(), server)
