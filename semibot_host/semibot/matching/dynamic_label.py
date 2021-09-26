# 履歴から生成されるラベル(動的ラベル)
# クラスメソッドで動作を書いていく
from typing import List
from .matching_pb import type_pb2

class DynamicLabel:
    @classmethod
    def recent_joined(cls,
                      personal_data: List[type_pb2.PersonalData],
                      task_request_history: List[type_pb2.TaskRequestData]):
        pass

    @classmethod
    def past_joined(cls,
                    personal_data: List[type_pb2.PersonalData],
                    task_request_history: List[type_pb2.TaskRequestData]):
        pass