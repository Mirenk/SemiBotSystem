import grpc
from matching_pb import data_manage_pb2, data_manage_pb2_grpc, type_pb2
from django.conf import settings

##
## データ管理システムから各データを取得するクラス
##
## MATCHING_DATAMANAGE_HOSTの環境変数で接続先変更
##

# ラベル辞書取得
def get_label_dict():
    with grpc.insecure_channel(settings.MATCHING_DATAMANAGE_HOST) as channel:
        stub = data_manage_pb2_grpc.DataManageStub(channel)
        res = stub.ListLabels(data_manage_pb2.ListLabelsRequest())

    return res.labels

# 個人情報辞書取得
def get_personal_data_dict():
    with grpc.insecure_channel(settings.MATCHING_DATAMANAGE_HOST) as channel:
        stub = data_manage_pb2_grpc.DataManageStub(channel)
        res = stub.ListPersonalData(data_manage_pb2.ListPersonalDataRequest())

    return res.personal_data

# 作業辞書取得
def get_task_list():
    with grpc.insecure_channel(settings.MATCHING_DATAMANAGE_HOST) as channel:
        stub = data_manage_pb2_grpc.DataManageStub(channel)
        res = stub.ListTasks(data_manage_pb2.ListTasksRequest())

    return res.tasks

# 上記関数を使い、名前のtype_pb2.Taskオブジェクトを返す関数
def get_task_from_name(name: str):
    with grpc.insecure_channel(settings.MATCHING_DATAMANAGE_HOST) as channel:
        stub = data_manage_pb2_grpc.DataManageStub(channel)
        res = stub.GetTaskFromName(data_manage_pb2.GetTaskFromNameRequest(name=name))

    return res

# 作業オブジェクトに対応した作業履歴を取得
def get_task_request_histories(task: type_pb2.Task):
    with grpc.insecure_channel(settings.MATCHING_DATAMANAGE_HOST) as channel:
        stub = data_manage_pb2_grpc.DataManageStub(channel)
        res = stub.GetTaskRequestHistories(task)

    return res.task_requests