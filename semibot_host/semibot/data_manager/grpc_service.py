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

    def ListLabels(self, request, context):
        response = data_manage_pb2.ListLabelsResponse()
        labels_pb = self.__get_label_pb_list_from_label_queryset(Label.objects.all())

        response.labels.extend(labels_pb)

        return response

    def ListCandidates(self, request, context):
        pass

    def ListTasks(self, request, context):
        pass

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
