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

    # 回数ラベル
    # これは他のラベル付けで使う用
    # PersonalData.idをキー、回数をvalueとする辞書で返す
    @classmethod
    def __join_count(cls,
                    personal_data: dict[str, type_pb2.PersonalData],
                    task_request_history: List[type_pb2.TaskRequestData]):
        user_dict = {}
        for key in personal_data.keys():
            user_dict[key] = 0

        for task_request in task_request_history:
            for worker in task_request.worker.values():
                user_dict[worker.id] = user_dict[worker.id] + 1

        return user_dict

    # 回数が少ない順に大きい動的ラベル
    @classmethod
    def few_join(cls,
                 personal_data: dict[str, type_pb2.PersonalData],
                 task_request_history: List[type_pb2.TaskRequestData]):

        user_dict = cls.__join_count(personal_data, task_request_history)
        # ラベル付け
        label = type_pb2.Label(name='join_count')
        var_label = type_pb2.LabelValue()
        var_label.label.CopyFrom(label)
        for id, count in user_dict.items():
            var_label.value = -count
            personal_data[id].var_labels.append(var_label)

        return personal_data

    # 他のラベル処理で使う用
    # PersonalData.idをキー、timestampをvalueとする辞書で返す
    @classmethod
    def __last_join_date(cls,
                    personal_data: dict[type_pb2.PersonalData],
                    task_request_history: List[type_pb2.TaskRequestData]):
        user_dict = {}
        for key in personal_data.keys():
            user_dict[key] = 0

        for task_request in task_request_history:
            for worker in task_request.worker.values():
                if user_dict[worker.id] < task_request.task_date.seconds:
                    user_dict[worker.id] = task_request.task_date.seconds

        return user_dict

    # 参加日時が古い順に大きい動的ラベル
    @classmethod
    def past_joined(cls,
                    personal_data: dict[type_pb2.PersonalData],
                    task_request_history: List[type_pb2.TaskRequestData]):

        user_dict = cls.__last_join_date(personal_data, task_request_history)
        # ラベル付け
        label = type_pb2.Label(name='past_joined')
        var_label = type_pb2.LabelValue()
        var_label.label.CopyFrom(label)
        for id, timestamp in user_dict.items():
            var_label.value = -timestamp
            personal_data[id].var_labels.append(var_label)

        return personal_data

    # 最近参加した人につけるラベル
    # 動的か静的かは今のところ未定(ゼミ管理に使わないので…)
    @classmethod
    def recent_joined(cls,
                      personal_data: dict[type_pb2.PersonalData],
                      task_request_history: List[type_pb2.TaskRequestData]):
            pass