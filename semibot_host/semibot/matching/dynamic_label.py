# 履歴から生成されるラベル(動的ラベル)
# クラスメソッドで動作を書いていく
from typing import List
from .matching_pb import type_pb2

class DynamicLabel:
    """
    メソッド追加方法
    @classmethod
    def メソッド名(cls,
                personal_data: List[type_pb2.PersonalData],
                task_request_history: List[type_pb2.TaskRequestData]):
        ~処理~

    type_pb2.PersonalDataのlabelsかvar_labelsにつける。
    var_labelsの場合、数値が大きいものが優先される。
    """

    # 最近参加した人につけるラベル
    # 動的か静的かは今のところ未定(ゼミ管理に使わないので…)
    @classmethod
    def recent_joined(cls,
                      personal_data: List[type_pb2.PersonalData],
                      task_request_history: List[type_pb2.TaskRequestData]):
        pass

    # 参加数が少なく、参加日時が古い人につける動的ラベル
    # 参加数が他の人より多い場合はつけない
    # 最大値が10、日時が新しくなる毎に少なくなる
    @classmethod
    def past_joined(cls,
                    personal_data: List[type_pb2.PersonalData],
                    task_request_history: List[type_pb2.TaskRequestData]):
        pass