from .models import *

from matching_pb import data_manage_pb2, data_manage_pb2_grpc, type_pb2

# サービス定義
class DataManage(data_manage_pb2_grpc.DataManageServicer):
    def ListLabels(self, request, context):
        response = data_manage_pb2.ListLabelsResponse()
        labels = Label.objects.all()

        for label in labels:
            label_pb = type_pb2.Label(name=label.name)
            response.labels.append(label_pb)

        return response